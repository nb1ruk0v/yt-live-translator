#!/usr/bin/env bash
# Sync code → run command on remote → pull data/ back.
#
# Required env (in .env):
#   REMOTE_HOST       user@host for SSH
# Optional env:
#   REMOTE_DIR        path to repo on server (default: ~/vt-claude)
#   VT_DATA_LOCAL     where to put pulled artifacts locally (default: data)
#
# Usage:
#   ./run_remote.sh uv run pytest
#   ./run_remote.sh --sync-data uv run src/dub.py "data/foo.mp4"
#   ./run_remote.sh uv run src/dub.py "https://youtu.be/..."
#
# Server pre-requisites (one-time setup):
#   - uv, ffmpeg in PATH
#   - ollama serve + `ollama pull gemma4:e4b`
#   - NVIDIA driver + CUDA toolkit for torch
#   - .env on server with HUGGINGFACE_TOKEN
#   - config.yaml on server with device: cuda
#   - git clone <repo> $REMOTE_DIR && cd $REMOTE_DIR && uv sync

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ -f "$ROOT/.env" ]]; then
    # shellcheck disable=SC1091
    source "$ROOT/.env"
fi

if [[ -z "${REMOTE_HOST:-}" ]]; then
    echo "Error: REMOTE_HOST not set. Add it to .env, e.g.:" >&2
    echo "  REMOTE_HOST=user@gpu-host" >&2
    exit 1
fi
REMOTE_DIR="${REMOTE_DIR:-~/vt-claude}"
VT_DATA_LOCAL="${VT_DATA_LOCAL:-data}"

SYNC_DATA=false
if [[ "${1:-}" == "--sync-data" ]]; then
    SYNC_DATA=true
    shift
fi

if [[ $# -eq 0 ]]; then
    echo "Usage: ./run_remote.sh [--sync-data] <command...>" >&2
    echo "Examples:" >&2
    echo "  ./run_remote.sh uv run pytest" >&2
    echo "  ./run_remote.sh --sync-data uv run src/dub.py \"data/foo.mp4\"" >&2
    echo "  ./run_remote.sh uv run src/dub.py \"https://youtu.be/...\"" >&2
    exit 1
fi

echo "==> rsync code → ${REMOTE_HOST}:${REMOTE_DIR}"
rsync -az --progress \
    --exclude='.git/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='.venv/' \
    --exclude='.pytest_cache/' \
    --exclude='.ruff_cache/' \
    --exclude='data/' \
    --exclude='experiments/' \
    --exclude='.DS_Store' \
    --exclude='.env' \
    --exclude='config.yaml' \
    . "${REMOTE_HOST}:${REMOTE_DIR}"

if [[ "${SYNC_DATA}" == true ]]; then
    echo "==> rsync data/ → ${REMOTE_HOST}:${REMOTE_DIR}/data/"
    rsync -az --progress data/ "${REMOTE_HOST}:${REMOTE_DIR}/data/"
fi

# Quote each positional arg with printf '%q' so word boundaries (esp. paths
# with spaces) survive transit through ssh + bash -lc parsing.
REMOTE_CMD=$(printf '%q ' "$@")
echo "==> Remote: $*"
ssh -t "${REMOTE_HOST}" "bash -lc 'cd ${REMOTE_DIR} && ${REMOTE_CMD}'"

echo "==> rsync ${REMOTE_HOST}:${REMOTE_DIR}/data/ → ${VT_DATA_LOCAL}/"
mkdir -p "${VT_DATA_LOCAL}"
rsync -az --progress "${REMOTE_HOST}:${REMOTE_DIR}/data/" "${VT_DATA_LOCAL}/"
