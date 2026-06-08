from unittest.mock import MagicMock, patch

from merge import (
    ATEMPO_MAX,
    AUDIO_SOFT,
    VIDEO_MIN,
    _plan_segment,
    merge,
    plan_timeline,
)
from segment import Segment


def make_segments():
    return [
        Segment(
            start=0.0,
            end=2.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/seg_0000.wav",
            audio_duration=1.8,
        ),
        Segment(
            start=3.0,
            end=5.0,
            original="Bye",
            translated="Пока",
            audio_path="/tmp/seg_0001.wav",
            audio_duration=1.5,
        ),
    ]


def _setup(mock_ffmpeg, video_total=20.0):
    """Self-returning audio + video chains so all filter calls land on one mock each."""
    audio_chain = MagicMock()
    audio_chain.filter.return_value = audio_chain
    video_chain = MagicMock()
    video_chain.filter.return_value = video_chain
    input_mock = MagicMock()
    input_mock.audio = audio_chain
    input_mock.video = video_chain
    mock_ffmpeg.input.return_value = input_mock
    mock_ffmpeg.probe.return_value = {"format": {"duration": str(video_total)}}
    mock_ffmpeg.concat.return_value = MagicMock()
    mock_ffmpeg.filter.return_value = MagicMock()
    mock_out = MagicMock()
    mock_ffmpeg.output.return_value = mock_out
    mock_out.overwrite_output.return_value = mock_out
    return audio_chain, video_chain


def _filter_names(audio_chain):
    return [c.args[0] for c in audio_chain.filter.call_args_list]


@patch("merge.ffmpeg")
def test_merge_returns_output_path_with_suffix(mock_ffmpeg):
    _setup(mock_ffmpeg)
    result = merge("/videos/test.mp4", make_segments(), "_dubbed")
    assert result == "/videos/test_dubbed.mp4"


@patch("merge.ffmpeg")
def test_merge_regenerates_audio_pts_after_amix(mock_ffmpeg):
    # amix over many adelay'd streams can emit a corrupt PTS the mp4 muxer rejects
    # ("non-monotonic DTS ... INT64_MAX"). The mixed audio must be passed through
    # asetpts=N/SR/TB to regenerate clean timestamps before muxing.
    _setup(mock_ffmpeg)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    amix_out = mock_ffmpeg.filter.return_value  # ffmpeg.filter(..., "amix", ...) result
    asetpts_calls = [c for c in amix_out.filter.call_args_list if c.args[0] == "asetpts"]
    assert asetpts_calls, "mixed audio must be re-stamped with asetpts after amix"
    assert asetpts_calls[0].args[1] == "N/SR/TB"


@patch("merge.ffmpeg")
def test_merge_no_filters_when_audio_fits_window(mock_ffmpeg):
    # video_total=20 → both segments' windows easily fit their audio
    audio_chain, _ = _setup(mock_ffmpeg, video_total=20.0)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    names = _filter_names(audio_chain)
    assert "atrim" not in names
    assert "atempo" not in names


@patch("merge.ffmpeg")
def test_merge_slows_video_when_audio_overflows(mock_ffmpeg):
    # seg0 [0,2) w=2 with a=3.0 → video slowed (setpts factor target/w), audio at soft cap, no atrim
    audio_chain, video_chain = _setup(mock_ffmpeg, video_total=4.0)
    segs = [_seg(0.0, 2.0, 3.0), _seg(2.0, 4.0, 1.0)]
    merge("/videos/test.mp4", segs, "_dubbed")

    # video was slowed: a setpts call carries the timestamp-resetting form (PTS-STARTPTS)*factor
    setpts_args = [c.args[1] for c in video_chain.filter.call_args_list if c.args[0] == "setpts"]
    assert any(str(a).startswith("(PTS-STARTPTS)*") for a in setpts_args)
    # audio softly sped, not trimmed (target exactly fits the sped audio)
    anames = _filter_names(audio_chain)
    assert "atempo" in anames
    assert "atrim" not in anames


@patch("merge.ffmpeg")
def test_merge_trims_only_on_truncation(mock_ffmpeg):
    # huge deficit on seg0 → video floored, audio at ATEMPO_MAX, tail trimmed → atrim present
    audio_chain, _ = _setup(mock_ffmpeg, video_total=4.0)
    segs = [_seg(0.0, 2.0, 10.0), _seg(2.0, 4.0, 0.5)]
    merge("/videos/test.mp4", segs, "_dubbed")

    atempo_calls = [c for c in audio_chain.filter.call_args_list if c.args[0] == "atempo"]
    atrim_calls = [c for c in audio_chain.filter.call_args_list if c.args[0] == "atrim"]
    assert abs(atempo_calls[0].args[1] - ATEMPO_MAX) < 1e-6
    assert len(atrim_calls) == 1  # only the truncated segment is capped


@patch("merge.ffmpeg")
def test_merge_audio_delayed_to_shifted_offset(mock_ffmpeg):
    # seg0 slowed to target 2.4 → seg1 adelay must reflect new_start=2400ms, not original 2000ms
    audio_chain, _ = _setup(mock_ffmpeg, video_total=4.0)
    segs = [_seg(0.0, 2.0, 3.0), _seg(2.0, 4.0, 1.0)]
    merge("/videos/test.mp4", segs, "_dubbed")

    adelay_calls = [c for c in audio_chain.filter.call_args_list if c.args[0] == "adelay"]
    expected_ms = int((3.0 / AUDIO_SOFT) * 1000)  # 2400
    assert any(f"{expected_ms}|{expected_ms}" == c.args[1] for c in adelay_calls)


def test_plan_segment_fits_natural():
    # audio shorter than window → no speedup, no slowdown
    p = _plan_segment(a=1.5, w=2.0)
    assert p.audio_tempo == 1.0
    assert p.video_speed == 1.0
    assert p.target_dur == 2.0
    assert p.truncated == 0.0


def test_plan_segment_soft_audio_only():
    # a/w = 1.2 (< AUDIO_SOFT=1.25): soft speedup alone makes it fit, video untouched
    p = _plan_segment(a=2.4, w=2.0)
    assert abs(p.audio_tempo - 1.2) < 1e-6
    assert p.video_speed == 1.0
    assert p.target_dur == 2.0
    assert p.truncated == 0.0


def test_plan_segment_slows_video():
    # a/w = 1.5 > AUDIO_SOFT: audio capped at 1.25, video slowed to fit, no truncation
    p = _plan_segment(a=3.0, w=2.0)
    assert abs(p.audio_tempo - AUDIO_SOFT) < 1e-6
    needed = 3.0 / AUDIO_SOFT  # 2.4
    assert abs(p.target_dur - needed) < 1e-6
    assert abs(p.video_speed - 2.0 / needed) < 1e-6  # 0.8333
    assert p.video_speed >= VIDEO_MIN
    assert p.truncated == 0.0


def test_plan_segment_hits_video_floor_then_hard_audio():
    # huge deficit: video pinned at VIDEO_MIN floor, audio re-sped up to ATEMPO_MAX, tail trimmed
    p = _plan_segment(a=10.0, w=2.0)
    assert p.video_speed == VIDEO_MIN
    target = 2.0 / VIDEO_MIN  # 4.0
    assert abs(p.target_dur - target) < 1e-6
    assert abs(p.audio_tempo - ATEMPO_MAX) < 1e-6
    assert abs(p.truncated - (10.0 / ATEMPO_MAX - target)) < 1e-6  # > 0
    assert p.truncated > 0


def test_plan_segment_nonpositive_window_overflows():
    # w <= 0 (overlapping/broken timings): target 0, no slowdown, audio overflows
    p = _plan_segment(a=3.0, w=0.0)
    assert p.target_dur == 0.0
    assert p.video_speed == 1.0
    assert p.audio_tempo == 1.0


def _seg(start, end, a):
    return Segment(
        start=start,
        end=end,
        original="x",
        translated="ы",
        audio_path="/tmp/x.wav",
        audio_duration=a,
    )


def test_plan_timeline_cumulative_new_start():
    # seg0 window [0,3) w=3 fits a=1.8 → target 3; seg1 last window [3,5) w=2 fits a=1.5 → target 2
    segs = [_seg(0.0, 2.0, 1.8), _seg(3.0, 5.0, 1.5)]
    plans = plan_timeline(segs, video_total=5.0)
    assert plans[0].new_start == 0.0
    assert plans[0].target_dur == 3.0
    assert plans[1].new_start == 3.0  # 0 + target_dur[0]


def test_plan_timeline_slowdown_shifts_later_segments():
    # seg0 [0,2) w=2 with a=3.0: audio capped at AUDIO_SOFT, video slowed (vspeed~0.83),
    # so target = needed = 3/AUDIO_SOFT = 2.4
    # seg1 must start at 2.4, not at its original 2.0
    segs = [_seg(0.0, 2.0, 3.0), _seg(2.0, 4.0, 1.0)]
    plans = plan_timeline(segs, video_total=4.0)
    assert abs(plans[0].target_dur - 3.0 / AUDIO_SOFT) < 1e-6
    assert abs(plans[1].new_start - 3.0 / AUDIO_SOFT) < 1e-6


def test_plan_timeline_last_window_uses_video_total():
    # single segment, window = video_total - start = 4.0; a=3.0 fits → no stretch
    plans = plan_timeline([_seg(1.0, 2.0, 3.0)], video_total=5.0)
    assert plans[0].target_dur == 4.0
    assert plans[0].new_start == 1.0  # preroll offset preserved
    assert plans[0].video_speed == 1.0


def test_plan_timeline_empty():
    assert plan_timeline([], video_total=5.0) == []


@patch("merge.ffmpeg")
def test_merge_last_segment_overflow_is_slowed(mock_ffmpeg):
    # single segment whose audio (3.0s) overflows its window [0, video_total=2.0]:
    # the last window is now bounded by video_total and participates in the cascade,
    # so the video is slowed (setpts factor) rather than left untouched.
    audio_chain, video_chain = _setup(mock_ffmpeg, video_total=2.0)
    segs = [_seg(0.0, 1.0, 3.0)]
    merge("/videos/test.mp4", segs, "_dubbed")

    setpts_args = [c.args[1] for c in video_chain.filter.call_args_list if c.args[0] == "setpts"]
    assert any(str(a).startswith("(PTS-STARTPTS)*") for a in setpts_args)
