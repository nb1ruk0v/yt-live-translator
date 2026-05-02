# Mastering Claude Code in 30 minutes.mp4

## [00:18.130 → 00:24.670] dur=6.54s

**EN:** Hey, everyone. I'm Boris. I'm a member of technical staff here at Anthropic, and I created QuadCode.
**gemma:** Всем привет. Я Борис. Я технический сотрудник Anthropic и создатель QuadCode.
**aya:** Привет всем. Меня зовут Борис. Я член технической команды в Антропике и создал КвадКод.

## [00:25.390 → 00:29.450] dur=4.06s

**EN:** And here to talk to you a little bit about some practical tips and tricks for using QuadCode.
**gemma:** И сегодня я расскажу вам о практических советах и хитростях использования QuadCode.
**aya:** И вот я расскажу вам несколько практических советов и трюков по использованию КвадКода.

## [00:30.610 → 00:35.630] dur=5.02s

**EN:** It's going to be very practical. I'm not going to go too much into the history or the theory or anything like this.
**gemma:** Это будет очень практично. Я не буду углубляться в историю или теорию.
**aya:** Я предоставлю очень практические советы, не углубляясь в историю или теорию.

## [00:37.210 → 00:41.510] dur=4.30s

**EN:** And yeah, before we start, actually, can we get a quick show of hands who has used QuadCode before?
**gemma:** И да, прежде чем мы начнем, поднимем руки, кто уже пользовался QuadCode?
**aya:** Прежде чем начать, быстро: кто из вас уже использовал QuadCode?

## [00:43.800 → 00:45.360] dur=1.56s

**EN:** Yeah. All right. That's what we like to see.
**gemma:** Хорошо. Это то, что мы хотели увидеть.
**aya:** Отлично! Мы рады этому.

## [00:45.940 → 00:47.660] dur=1.72s

**EN:** For everyone that didn't raise your hands,
**gemma:** Для тех, кто не поднял руки,
**aya:** Для тех, кто не поднял руку:

## [00:48.120 → 00:53.520] dur=5.40s

**EN:** I know you're not supposed to do this while people are talking, but if you can open your laptop and type this,
**gemma:** Я знаю, что нельзя делать это во время разговора, но если вы можете открыть ноутбук и напечатать это,
**aya:** Я знаю, что обычно не следует делать это во время речи, но если вы можете открыть ноутбук и ввести следующее:

## [00:57.460 → 01:01.420] dur=3.96s

**EN:** and this will help you install QuadCode just so you can follow along for the rest of the talk.
**gemma:** это поможет вам установить QuadCode, чтобы вы могли следить за остальной частью разговора.
**aya:** и это поможет вам установить QuadCode, чтобы вы могли следить за остальной частью выступления.

## [01:07.120 → 01:16.140] dur=9.02s

**EN:** All you need is Node.js if you have it. This should work. Yeah.
**gemma:** Вам нужен только Node.js, если он у вас есть. Это должно сработать. Да.
**aya:** Вам нужно только Node.js, если у вас он установлен. Это должно работать. Да.

## [01:16.460 → 01:19.480] dur=3.02s

**EN:** You don't have to follow along, but if you don't have it yet,
**gemma:** Вам не обязательно следить, но если у вас его еще нет,
**aya:** Вы не обязаны следить за этим, но если у вас его ещё нет,

## [01:20.080 → 01:22.220] dur=2.14s

**EN:** yeah, this is your chance to install it so you can follow along.
**gemma:** да, это ваш шанс установить его, чтобы вы могли следить.
**aya:** да, это ваш шанс установить его, чтобы вы могли следить дальше.

## [01:25.610 → 01:26.650] dur=1.04s

**EN:** So what is QuadCode?
**gemma:** Так что такое QuadCode?
**aya:** QuadCode — это гипотетический или специализированный код, используемый в определенных технологических контекстах (например, в разработке программного обеспечения). Он может представлять собой структурированную систему из четырёх элементов (отсюда "Quad" — по-русски "четвёрка") для более эффективного и чёткого представления данных или команд.

## [01:27.430 → 01:34.010] dur=6.58s

**EN:** QuadCode is a new kind of AI assistant, and there's been different generations of AI assistants for coding.
**gemma:** QuadCode — это новый тип помощника с ИИ, и уже были разные поколения таких помощников для кодирования.
**aya:** QuadCode — это новый вид ассистента искусственного интеллекта, и на протяжении лет существовало различные поколения ассистентов ИИ для программирования.

## [01:34.450 → 01:39.490] dur=5.04s

**EN:** Most of them have been about completing, you know, like a line at a time, completing a few lines of code at a time.
**gemma:** Большинство из них были посвящены дополнению, знаете, построчно, дополнению нескольких строк кода.
**aya:** Большинство из них фокусировались на автодополнении кода, то есть завершении строк или блоков кода по мере их ввода.

## [01:40.270 → 01:47.570] dur=7.30s

**EN:** QuadCode is not for that. It's fully agentic. So it's meant for building features, for writing entire functions, entire files,
**gemma:** QuadCode не для этого. Он полностью агентный. Он предназначен для создания функций, написания целых файлов.
**aya:** QuadCode не предназначен для автодополнения строк кода. Он представляет собой полностью автономное решение, предназначенное для создания функций и целых файлов, а не просто для завершения отдельных строк.

## [01:48.490 → 01:50.650] dur=2.16s

**EN:** fixing entire bugs at the same time.
**gemma:** и исправления целых ошибок одновременно.
**aya:** и одновременного устранения ошибок в коде.

## [01:52.170 → 01:55.570] dur=3.40s

**EN:** And what's kind of cool about QuadCode is it works with all of your tools.
**gemma:** И что круто в QuadCode — он работает со всеми вашими инструментами.
**aya:** И что круто в QuadCode, он работает со всеми вашими инструментами.

## [01:55.910 → 02:04.170] dur=8.26s

**EN:** And you don't have to change out your workflow. You don't have to swap everything to start using it. So whatever IDE you use, if you use VS code, or if you use X code,
**gemma:** И вам не нужно менять рабочий процесс. Не нужно отказываться от всего, чтобы начать им пользоваться. Так что какую бы IDE вы ни использовали, будь то VS Code или Xcode,
**aya:** И вы не должны менять свой рабочий процесс. Не нужно переключаться на что-то новое, чтобы начать использовать QuadCode. Он совместим с любой вашей средой разработки — будь то Visual Studio Code или Xcode.

## [02:04.770 → 02:16.470] dur=11.70s

**EN:** or if you use JetBrains IDEs, there's some people at Anthropic that you can't pry them from their cold, dead hands, but they use QuadCode because QuadCode works with every single IDE, every terminal out there.
**gemma:** или если вы используете IDE от JetBrains, есть люди в Anthropic, от которых невозможно оторвать, но они используют QuadCode, потому что он работает со всеми IDE и всеми терминалами.
**aya:** или если вы используете IDE от JetBrains — у некоторых людей в Anthropic их просто не оторвать от любимых инструментов, но они используют QuadCode, потому что он совместим с любой IDE и терминалом.

## [02:17.250 → 02:22.230] dur=4.98s

**EN:** It'll work locally over remote SSH, over Tmux, whatever environment you're in,
**gemma:** Он будет работать локально, через удаленный SSH, через Tmux — в любой среде,
**aya:** Он будет работать локально через удалённый SSH, в Tmux или любой другой среде.

## [02:22.730 → 02:27.570] dur=4.84s

**EN:** you can run it. It's general purpose.
**gemma:** вы можете его запустить. Он универсальный.
**aya:** Его универсальность позволяет запускать его в любых условиях.

## [02:28.070 → 02:39.810] dur=11.74s

**EN:** And this is something where if you haven't used these kind of freeform coding assistants in the past, it can be kind of hard to figure out how to get started. Because you open it up, and you just see a prompt bar, and you might wonder, like, what do I do with this?
**gemma:** И это та вещь, где, если вы раньше не пользовались такими свободными помощниками по кодированию, может быть сложно понять, как начать. Потому что вы его открываете, и видите только строку запроса, и можете задуматься: а что мне с этим делать?
**aya:** И если вы раньше не использовали подобные ассистенты для кодирования, то может показаться сложным начать работу. Потому что при открытии вы видите только строку ввода, и можно задуматься: что с этим делать?

## [02:39.870 → 02:43.510] dur=3.64s

**EN:** What do I type in? It's a power tool. So you can use it for a lot of things.
**gemma:** Что мне написать? Это мощный инструмент. Поэтому вы можете использовать его для множества вещей.
**aya:** Что вводить? Это мощный инструмент, поэтому его можно использовать для множества задач.

## [02:44.130 → 02:47.930] dur=3.80s

**EN:** But also, because it can do so much, we don't try to guide you towards a particular workflow.
**gemma:** Но также, поскольку он может делать так много, мы не пытаемся направить вас к конкретному рабочему процессу.
**aya:** Но поскольку он может выполнять многое, мы не навязываем конкретный рабочий процесс.

## [02:48.290 → 02:51.650] dur=3.36s

**EN:** Because really, you should be able to use it however you want as an engineer.
**gemma:** Потому что на самом деле вы должны иметь возможность использовать его как хотите, будучи инженером.
**aya:** Поскольку в конечном счёте вы, как инженер, должны быть способны использовать его по своему усмотрению.

## [02:56.810 → 03:02.450] dur=5.64s

**EN:** As you open up QuadCode for the first time, there's a few things that we recommend doing to get your environment set up.
**gemma:** Когда вы впервые открываете QuadCode, есть несколько вещей, которые мы рекомендуем сделать, чтобы настроить вашу среду.
**aya:** При первом запуске QuadCode рекомендуется выполнить несколько шагов для настройки среды работы.

## [03:03.010 → 03:12.290] dur=9.28s

**EN:** And these are pretty straightforward. So run terminal setup, this will give you shift enter for new lines, so you don't have to do, like, backslashes to enter new lines. This is, you know, it makes it a little bit nicer to use.
**gemma:** И это довольно просто. Запустите настройку терминала — это даст вам Shift + Enter для переноса строк, так что вам не придется использовать обратные слэши. Это просто делает его удобнее в использовании.
**aya:** Это довольно просто: запустите настройку терминала, чтобы получить символ перехода на новую строку (Shift+Enter), что сделает работу с текстом удобнее.

## [03:12.910 → 03:16.970] dur=4.06s

**EN:** Do slash theme to set light mode or dark mode or adultanized themes.
**gemma:** Используйте слэш-тему, чтобы установить светлый или темный режим, или настроить другие темы.
**aya:** Используйте слэш для переключения между светлой, тёмной или персонализированными темами.

## [03:18.570 → 03:28.510] dur=9.94s

**EN:** You can do slash install GitHub app. So today, once we announced a GitHub app, where you can add mention Cloud on any GitHub issue or pull request.
**gemma:** Вы можете использовать /install GitHub app. Таким образом, после того, как мы анонсировали приложение GitHub, вы сможете добавлять упоминания Cloud в любые проблемы или запросы на слияние в GitHub.
**aya:** Установите приложение GitHub с помощью слэша. После запуска приложения вы сможете добавлять упоминания о Cloud в любые задачи или запросы на слияние на GitHub.

## [03:28.810 → 03:31.250] dur=2.44s

**EN:** So to install it, just run this command in your terminal.
**gemma:** Чтобы установить его, просто выполните эту команду в терминале.
**aya:** Чтобы установить приложение, просто выполните эту команду в терминале.

## [03:33.090 → 03:43.390] dur=10.30s

**EN:** You can customize the set of allowed tools that you can use, so you're not prompted for it every time. This is pretty convenient. For stuff that I'm prompted about a bunch, I'll definitely customize it in this way, so I don't have to accept it every time.
**gemma:** Вы можете настроить набор разрешенных инструментов, чтобы вам не приходилось подтверждать это каждый раз. Это очень удобно. Для вещей, о которых меня просят много раз, я обязательно настрою это таким образом, чтобы не принимать это каждый раз.
**aya:** Вы можете настроить набор разрешённых инструментов, чтобы не получать постоянные запросы на разрешение. Это очень удобно. Для часто встречающихся действий я обязательно настрою такие параметры, чтобы не подтверждать их каждый раз.

## [03:44.110 → 03:48.710] dur=4.60s

**EN:** And something that I actually do is, for a lot of my prompts, I won't hand type them into a Cloud Code.
**gemma:** И то, что я на самом деле делаю, это для многих своих запросов я не буду вводить их вручную в Cloud Code.
**aya:** И я действительно делаю так: для многих запросов я не вручную вводим их в кодовую среду Cloud.

## [03:49.250 → 03:55.230] dur=5.98s

**EN:** If you're on macOS, you can go into your system settings, under accessibility as dictation, and you can enable it.
**gemma:** Если вы на macOS, вы можете зайти в системные настройки, в раздел «Универсальный доступ» и включить его.
**aya:** Если вы используете macOS, перейдите в настройки системы → Диктовка (в разделе Доступность) и включите её.

## [03:55.810 → 04:00.390] dur=4.58s

**EN:** And so something I do is you just hit, like, the dictation key twice, and you can just speak your prompt.
**gemma:** И поэтому то, что я делаю, это просто нажимаю клавишу диктовки дважды, и могу просто проговорить свой запрос.
**aya:** И вы просто нажимаете клавишу диктовки дважды и говорите свой запрос.

## [04:01.550 → 04:09.610] dur=8.06s

**EN:** And it helps a lot to have specific prompts. So this is actually pretty awesome. You can just talk to Cloud Code and, like you would another engineer, and you don't have to type a lot of code.
**gemma:** И очень помогает иметь конкретные запросы. Это довольно круто. Вы можете просто поговорить с Cloud Code, как с другим инженером, и не нужно писать много кода.
**aya:** И наличие конкретных запросов очень помогает. Это действительно круто: вы можете общаться с Cloud Code так же, как с другим инженером, не тратя время на ввод большого количества кода.

## [04:14.070 → 04:19.050] dur=4.98s

**EN:** So when you're starting out with Cloud Code, it's so freeform, and it can do everything, what do you start with?
**gemma:** Когда вы только начинаете работать с Cloud Code, это очень свободно, и он может делать всё. С чего начать?
**aya:** Когда вы начинаете работу с Cloud Code, его гибкость позволяет выполнять всё что угодно. Но где начать? Попробуйте:

## [04:19.470 → 04:25.630] dur=6.16s

**EN:** The thing I recommend above everything else is starting with CodeBase Q&A. So just asking your question, asking questions to your CodeBase.
**gemma:** То, что я рекомендую больше всего, — это начать с Q&A по кодовой базе. Просто задавать вопросы своей кодовой базе.
**aya:** Я рекомендую начать с CodeBase Q&A. Задавайте вопросы своей базе кода — это лучший способ освоиться.

## [04:26.490 → 04:29.070] dur=2.58s

**EN:** This is something that we teach new hires at Anthropic.
**gemma:** Это то, чему мы учим новых сотрудников в Anthropic.
**aya:** Это то, что мы учим новых сотрудников в Antropic.

## [04:29.550 → 04:37.270] dur=7.72s

**EN:** So on the first day in technical onboarding, you learn about Cloud Code, you download it, you get it set up, and then you immediately start asking questions about the CodeBase.
**gemma:** В первый день технического онбординга вы узнаете о Cloud Code, скачаете его, настроите, и сразу же начнете задавать вопросы о кодовой базе.
**aya:** В первый день технической адаптации вы изучаете Cloud Code, скачиваете и настраиваете его, а затем сразу начинаете задавать вопросы о базе кода.

## [04:37.910 → 04:41.690] dur=3.78s

**EN:** And in the past, when you were doing technical onboarding, it's something that taxes the team a lot,
**gemma:** Раньше, когда проходил технический онбординг, это сильно нагружало команду.
**aya:** В прошлом техническая адаптация была более обременительной для команды.

## [04:42.290 → 04:44.990] dur=2.70s

**EN:** right? You have to ask other engineers on the team questions.
**gemma:** Верно? Приходилось задавать вопросы другим инженерам в команде.
**aya:** Да, раньше новым сотрудникам приходилось задавать много вопросов другим инженерам в команде.

## [04:45.710 → 04:48.870] dur=3.16s

**EN:** You have to look around the code, and this takes a while. You have to figure out how to use the tools.
**gemma:** Приходилось изучать код, а это занимает много времени. Нужно было понять, как пользоваться инструментами.
**aya:** Нужно было изучать код и инструменты, что занимало много времени.

## [04:49.230 → 04:50.230] dur=1.00s

**EN:** This takes a long time.
**gemma:** Это занимает много времени.
**aya:** Это занимает много времени.

## [04:51.670 → 04:56.170] dur=4.50s

**EN:** With Cloud Code, you can just ask Cloud Code, and it'll explore the code base. It'll answer these kind of questions.
**gemma:** С помощью Cloud Code можно просто спросить у него, и он изучит кодовую базу. Он ответит на такие вопросы.
**aya:** С Cloud Code можно просто спросить Cloud Code, и он сам исследует кодовую базу, отвечая на такие вопросы.

## [04:56.830 → 05:01.710] dur=4.88s

**EN:** And so at Anthropic, onboarding used to take about two or three weeks for technical hires. It's now about two or three days.
**gemma:** Раньше в Anthropic адаптация для технических сотрудников занимала две-три недели. Теперь это занимает два-три дня.
**aya:** В компании Anthropic, время адаптации для технических специалистов сократилось с двух-трёх недель до двух-трёх дней благодаря использованию Cloud Code и других инструментов.

## [05:05.260 → 05:15.800] dur=10.54s

**EN:** What's also kind of cool about Q&A is we don't do any sort of indexing. So there's no remote database with your code. We don't upload it anywhere. Your code stays local. We do not train generative models on the code.
**gemma:** Что также здорово в Q&A — мы не делаем индексации. Нет удаленной базы данных с вашим кодом. Мы его никуда не загружаем. Ваш код остается локальным. Мы не обучаем генеративные модели на коде.
**aya:** Также интересно, что система Q&A не использует индексацию. Следовательно, нет удалённой базы кода. Мы не загружаем его нигде. Код остаётся локальным. Мы не обучаем генеративные модели на коде.

## [05:16.780 → 05:19.960] dur=3.18s

**EN:** So it's there. You control it. There's no indices or anything like this.
**gemma:** Значит, он здесь. Вы им управляете. Нет индексов или чего-то подобного.
**aya:** Таким образом, вы контролируете всё. Нет индексов или подобных элементов.

## [05:20.600 → 05:22.740] dur=2.14s

**EN:** And what that means is also there's no setup.
**gemma:** И это значит, что не нужно никаких настроек.
**aya:** И это означает отсутствие настройки.

## [05:23.040 → 05:27.360] dur=4.32s

**EN:** So you start Cloud. You download it. You start it. There's no indexing. You don't have to wait. You can just use it right away.
**gemma:** Вы просто запускаете Cloud. Скачиваете его и начинаете. Нет индексации. Не нужно ждать, можно сразу пользоваться.
**aya:** Вы запускаете Cloud, скачиваете его и начинаете использовать сразу. Нет необходимости в индексации, нет ожидания.

## [05:30.310 → 05:38.450] dur=8.14s

**EN:** This is a technical talk. So I'm going to show some very specific prompts and very specific code samples that you can use and hopefully improve and up-level your Cloud Code experience.
**gemma:** Это технический разговор. Поэтому я покажу очень конкретные запросы и примеры кода, которые вы сможете использовать и, надеюсь, улучшить свой опыт работы с Cloud Code.
**aya:** Это техническая беседа. Я покажу некоторые очень конкретные запросы и примеры кода, которые вы можете использовать для улучшения и оптимизации опыта работы с кодом Cloud.

## [05:39.590 → 05:41.510] dur=1.92s

**EN:** So some kind of questions that you can ask is,
**gemma:** Так что вы можете спросить, это...
**aya:** Некоторые из вопросов, которые вы можете задать:

## [05:42.130 → 05:48.830] dur=6.70s

**EN:** you know, like, how is this particular piece of code used? Or how do I instantiate this thing? And Cloud Code, it won't just do like a text search and try to answer this.
**gemma:** Например, как используется этот конкретный фрагмент кода? Или как мне создать экземпляр этой вещи? И Cloud Code не просто выполнит поиск текста, чтобы ответить на это.
**aya:** Вы можете спрашивать, например: "Как используется этот фрагмент кода?" или "Как инициализировать это?" Cloud Code не просто выполняет текстовый поиск, он предоставляет конкретные ответы и примеры.

## [05:49.270 → 05:50.730] dur=1.46s

**EN:** It'll often go a level deeper.
**gemma:** Он часто углубляется на уровень выше.
**aya:** Он часто идёт глубже, предоставляя подробные объяснения и дополнительные контексты.

## [05:51.190 → 06:01.430] dur=10.24s

**EN:** And it'll try to find examples of how is this class instantiated? How is it used? And it'll give you a much deeper answer. So something that you would get out of a wiki or documentation instead of just like Command F.
**gemma:** И он попытается найти примеры того, как инстанцируется этот класс? Как он используется? И он даст вам гораздо более глубокий ответ. То, что вы получили бы из вики или документации, а не просто через Ctrl+F.
**aya:** Он ищет примеры инициализации и использования класса, предоставляя более глубокие ответы, аналогичные информации из вики или документации, а не просто результаты поиска по ключевым словам.

## [06:03.720 → 06:06.480] dur=2.76s

**EN:** Something that I do a lot also is ask it about Git history.
**gemma:** Я также часто прошу его рассказать об истории Git.
**aya:** Вы часто спрашиваете у него о истории Git-коммитов.

## [06:07.060 → 06:08.100] dur=1.04s

**EN:** So for example,
**gemma:** Например,
**aya:** Например, вы можете спросить: "Покажи мне историю коммитов для файла main.py в репозитории myproject с 2023 года".

## [06:08.600 → 06:12.620] dur=4.02s

**EN:** you know, why does this function have 15 arguments? And why are the arguments named this weird way?
**gemma:** Знаете, почему у этой функции 15 аргументов? И почему аргументы названы так странно?
**aya:** Вы знаете, почему у этой функции 15 аргументов? И почему они названы такими странными способами?

## [06:13.100 → 06:14.980] dur=1.88s

**EN:** And this is something I bet in all of our code bases.
**gemma:** И это то, что я подозреваю во всех наших кодовых базах.
**aya:** И это то, что, я уверен, присутствует во всех наших кодовых базах.

## [06:15.300 → 06:17.660] dur=2.36s

**EN:** You have some function like this or some class like this.
**gemma:** У вас есть функция или класс вроде этого.
**aya:** У вас есть функция подобная этой или класс подобный этому.

## [06:18.900 → 06:29.620] dur=10.72s

**EN:** And Cloud Code can look through Git history. And it'll look to figure out how did these arguments get introduced? And who introduced them? And what was the situation? What are the issues that those commits link to? And it'll look through all this and summarize it.
**gemma:** И Cloud Code может просмотреть историю Git. Он выяснит, как были введены эти аргументы? Кто их ввел? Какова была ситуация? К каким проблемам привязаны эти коммиты? Он проанализирует всё это и обобщит.
**aya:** И код в облаке может просматривать историю Git и определять, как были введены эти аргументы, кто их ввел и при каких обстоятельствах. Он ищет связанные с этим проблемы в коммитах и обобщает всю информацию.

## [06:29.760 → 06:32.480] dur=2.72s

**EN:** And you don't have to tell it that in all this detail.
**gemma:** И вам не нужно рассказывать ему все эти детали.
**aya:** И вам не нужно сообщать ему об этом во всех этих деталях.

## [06:32.920 → 06:42.900] dur=9.98s

**EN:** You just ask it. So just say, look through Git history. And it'll know to do this. The reason it knows, by the way, is not because we prompted it to. There's nothing in the system prompt about looking through Git history.
**gemma:** И вы просто спрашиваете его. Просто скажите: "Просмотри историю Git". И он сам это сделает. Причина, по которой он это знает, кстати, не в том, что мы ему об этом сказали. В системном промпте нет ничего о просмотре истории Git.
**aya:** Спроси его, чтобы оно просмотрело историю Git. И оно поймёт, что нужно сделать, не требуя дополнительных инструкций. В системе нет никаких подсказок о проверке истории Git.

## [06:43.260 → 06:44.880] dur=1.62s

**EN:** It knows it because the model is awesome.
**gemma:** Он это знает, потому что модель потрясающая.
**aya:** Оно так делает благодаря своему потрясающему алгоритму.

## [06:45.660 → 06:47.620] dur=1.96s

**EN:** And if you tell it to use Git, it'll know how to use Git.
**gemma:** И если вы скажете ему использовать Git, он будет знать, как это делать.
**aya:** Если вы дадите ему команду использовать Git, он сможет работать с этой системой контроля версий.

## [06:48.360 → 06:50.560] dur=2.20s

**EN:** So we're lucky to be building on such a good model.
**gemma:** Так что нам повезло строить на такой хорошей модели.
**aya:** Мы везём, что работаем с таким мощным алгоритмом.

## [06:52.320 → 06:55.140] dur=2.82s

**EN:** I often ask about GitHub issues.
**gemma:** Я часто спрашиваю о проблемах на GitHub.
**aya:** Я часто спрашиваю о проблемах на GitHub.

## [06:55.500 → 07:06.960] dur=11.46s

**EN:** So, you know, it can use webfetch and it can fetch issues and look up context on issues too. And this is pretty awesome. And this is something that I do every single Monday in our weekly standup.
**gemma:** Он может использовать webfetch, получать проблемы и искать контекст по ним. Это очень круто. Я делаю это каждую понедельник на нашем еженедельном стендапе.
**aya:** Так что оно умеет использовать webfetch для получения задач и поиска контекста в них. Это действительно круто. И я это делаю каждую понедельник на еженедельной встрече.

## [07:07.140 → 07:15.700] dur=8.56s

**EN:** I ask, what did I ship this week? And Quad Code looks to the log. It knows my username. And it'll just give me a nice readout of everything I shipped. And I'll just copy and paste that into a doc.
**gemma:** Я спрашиваю: что я выкатил на этой неделе? Quad Code смотрит в лог. Он знает мой ник и выдает мне красивый отчет обо всем, что я выкатил. А я просто копирую и вставляю это в документ.
**aya:** Я спрашиваю: "Что я выпустил на этой неделе?" И Quad Code обращается к логам, знает мой никнейм и предоставляет мне краткий отчёт о всём, что я выпустил. Я копирую и вставляю его в документ.

## [07:20.460 → 07:31.260] dur=10.80s

**EN:** So yeah, that's tip number one. For people that have not used Cloud Code before, if you're just showing it to someone for the first time, onboarding your team, the thing we definitely recommend is start with code base Q&A. Don't start by using fancy tools.
**gemma:** Итак, это первый совет. Если вы никогда не использовали Cloud Code, и только показываете его кому-то впервые, или обучаете команду, мы определенно рекомендуем начать с Q&A по кодовой базе. Не начинайте с использования сложных инструментов.
**aya:** Так что это первый совет. Для тех, кто не использовал Cloud Code раньше, при знакомстве команды с инструментом рекомендуем начать с базовых вопросов и ответов по кодовой базе, а не сразу переходить к сложным инструментам.

## [07:31.460 → 07:32.520] dur=1.06s

**EN:** Don't start by editing code.
**gemma:** Не начинайте с редактирования кода.
**aya:** Не начинайте с редактирования кода.

## [07:32.920 → 07:36.160] dur=3.24s

**EN:** Just start by asking questions about the code base. And that'll teach people how to prompt.
**gemma:** Просто начните с вопросов о кодовой базе. И это научит людей, как правильно формулировать запросы.
**aya:** Просто начните с вопросов о кодовой базе. Это научит людей формулировать запросы.

## [07:36.600 → 07:46.400] dur=9.80s

**EN:** And it'll start teaching them this boundary of, like, what can Cloud Code do? What is it capable of versus what do you need to hold its hand with a little bit more? What can be one-shotted, what can be two-shotted, three-shotted?
**gemma:** И это начнет обучать их границам: что может делать Cloud Code? Чем оно способно, и в чем ему нужна небольшая помощь? Что можно сделать за один, за два, за три запроса?
**aya:** И это поможет им понять границы возможностей Cloud Code: что он может сделать самостоятельно, а что требует более детального руководства. Что можно быстро решить, а что требует больше времени и внимания.

## [07:46.780 → 07:48.860] dur=2.08s

**EN:** What do you need to use interactive mode for in a REPL?
**gemma:** Для чего вам нужен интерактивный режим в REPL?
**aya:** Для использования интерактивного режима в REPL (Read-Evaluate-Print Loop) требуется: ... (требования могут варьироваться в зависимости от конкретной реализации, но обычно включают) ...

## [07:52.270 → 07:54.890] dur=2.62s

**EN:** Once you're pretty comfortable with Q&A, you can dive into editing code.
**gemma:** Когда вы освоите вопросы и ответы, вы сможете перейти к редактированию кода.
**aya:** После того как вы освоили вопросы и ответы, можно перейти к редактированию кода.

## [07:55.730 → 08:07.270] dur=11.54s

**EN:** This is the next thing. And the cool thing about any sort of agentic, you know, like, using an LM in an agentic way is you give it tools and it's just, like, magical. It figures out how to use the tools.
**gemma:** Это следующее. И классная вещь в любом агентивном использовании, знаете, когда вы используете языковую модель в таком режиме, — вы даете ей инструменты, и это просто волшебно. Она сама понимает, как ими пользоваться.
**aya:** Это следующий шаг. И крутое дело в использовании языковых моделей в агентном режиме: вы даете им инструменты, и они, как по магии, учатся их использовать.

## [08:07.870 → 08:14.990] dur=7.12s

**EN:** And with Cloud Code, we give it a pretty small set of tools. It's not a lot. And so it has a tool to edit files. It has a tool to run bash commands.
**gemma:** И с Cloud Code мы даем ей довольно небольшой набор инструментов. Это не много. У нее есть инструмент для редактирования файлов и инструмент для выполнения команд bash.
**aya:** С помощью Cloud Code предоставляется небольшой набор инструментов: возможность редактировать файлы и выполнять команды Bash.

## [08:15.330 → 08:16.810] dur=1.48s

**EN:** It has a tool to search files.
**gemma:** У нее есть инструмент для поиска файлов.
**aya:** Также у него есть инструмент для поиска файлов.

## [08:17.130 → 08:19.550] dur=2.42s

**EN:** And it'll string these together to explore the code,
**gemma:** И она объединит их, чтобы изучить код.
**aya:** И он объединяет эти инструменты для исследования кода,

## [08:20.830 → 08:22.490] dur=1.66s

**EN:** brainstorm, and then finally make edits.
**gemma:** Набросать идеи, а затем внести правки.
**aya:** для мозгового штурма и, в конечном итоге, внесения изменений.

## [08:23.690 → 08:32.130] dur=8.44s

**EN:** And you don't have to prompt it specifically to use this tool and this tool and this tool. You just say, you know, do this thing, and it'll figure out how to do it. It'll string it together in the right way that makes sense for Cloud Code.
**gemma:** И вам не нужно просить его конкретно использовать этот инструмент, этот инструмент и этот инструмент. Вы просто говорите: "Сделай это", и он сам поймет, как это сделать. Он объединит это в правильном порядке, который подходит для Cloud Code.
**aya:** И вам не нужно специально вызывать каждый инструмент по очереди. Достаточно дать команду, и он сам определит, какие инструменты использовать, чтобы выполнить задачу, логично интегрируя их для работы в облачном коде.

## [08:36.900 → 08:46.100] dur=9.20s

**EN:** There's a lot of ways to use this. Something I like to do sometimes is before having Cloud jump in to write code, I'll ask it to brainstorm a little bit or make a plan.
**gemma:** Есть много способов использовать это. Иногда я прошу его набросать идеи или составить план, прежде чем он начнет писать код.
**aya:** Есть множество способов использования этой технологии. Иногда я, например, перед тем как попросить облачный код написать код, прошу его сначала сгенерировать идеи или составить план.

## [08:46.920 → 08:48.380] dur=1.46s

**EN:** This is something we highly recommend.
**gemma:** Мы это очень рекомендуем.
**aya:** Это что-то, что мы настоятельно рекомендуем.

## [08:48.720 → 08:56.220] dur=7.50s

**EN:** And something I see sometimes is people, you know, they take Cloud Code and they ask it, hey, implement this enormous, like, 3000 line feature.
**gemma:** Иногда я вижу, что люди дают Cloud Code и просят его реализовать огромную функцию из 3000 строк.
**aya:** И часто люди используют облачный код, например, запрашивая у него реализацию большой функции из 3000 строк кода.

## [08:56.600 → 08:58.480] dur=1.88s

**EN:** And sometimes it gets this right on the first shot.
**gemma:** Иногда он делает это с первого раза.
**aya:** И иногда он выполняет это идеально с первого раза.

## [08:59.000 → 09:02.560] dur=3.56s

**EN:** But sometimes what happens is the thing that it builds is not at all the thing that you wanted.
**gemma:** Но иногда то, что он создает, совсем не то, что вы хотели.
**aya:** Но иногда получается, что то, что он строит, совсем не то, что вы хотели.

## [09:03.180 → 09:07.420] dur=4.24s

**EN:** And the easiest way to get the result you want is ask it to think first.
**gemma:** И самый простой способ получить желаемый результат — попросить его сначала подумать.
**aya:** И самый простой способ получить желаемый результат — попросить его сначала подумать.

## [09:07.900 → 09:12.400] dur=4.50s

**EN:** So brainstorm ideas, make a plan, run it by me, ask for approval before you write code.
**gemma:** Поэтому сначала генерируйте идеи, составьте план, покажите мне и получите одобрение, прежде чем писать код.
**aya:** Сначала генерируйте идеи, составьте план, представьте его мне, получите одобрение, прежде чем писать код.

## [09:13.100 → 09:21.440] dur=8.34s

**EN:** And you don't have to use plan mode. You don't have to use any special tools to do this. All you have to do is ask Cloud and it'll know to do this. So just say, before you write code, make a plan.
**gemma:** И вам не нужно использовать режим планирования. Не нужно использовать никаких специальных инструментов. Вам просто нужно попросить Cloud, и он поймет, что делать. Просто скажите: «Прежде чем писать код, составь план».
**aya:** И вы не обязаны использовать режим планирования. Не нужно никаких специальных инструментов — просто спросите Облако, и оно само поймёт, что нужно сделать. Достаточно сказать: «Перед написанием кода составьте план».

## [09:21.980 → 09:32.670] dur=10.69s

**EN:** That's it. This is also, I want to think for this one, this commit push VR, this is a really common incantation that I use. There's nothing special about it, but Cloud is kind of smart enough to interpret this.
**gemma:** Вот и всё. Я также хочу подумать над этим. Эта фраза «commit push VR» — очень распространенное заклинание, которое я использую. В ней нет ничего особенного, но Cloud достаточно умен, чтобы это интерпретировать.
**aya:** И это всё. Это также является распространённым заклинанием, которое я использую: «Подумать о коммите и пуше в VR». В нём нет ничего особенного, но Облако достаточно умное, чтобы интерпретировать его.

## [09:32.790 → 09:36.490] dur=3.70s

**EN:** So it'll make a commit, it'll push it to the branch, make a branch, and then make a pull request for me on GitHub.
**gemma:** Он сделает коммит, отправит его в ветку, создаст ветку и затем сделает для меня запрос на слияние в GitHub.
**aya:** Он создаст коммит, отправит его в ветку, затем создаст новую ветку и сделает запрос на слияние (pull request) на GitHub.

## [09:36.950 → 09:45.890] dur=8.94s

**EN:** You don't have to explain anything. It'll look through the code, it'll look through the history, it'll look through the Git log by itself to figure out the commit format and all the stuff. And it'll make the commit and push it the right way.
**gemma:** Вам не нужно ничего объяснять. Он сам проанализирует код, историю, журнал Git и поймет формат коммита и все остальные детали. И сделает коммит и отправит его правильно.
**aya:** Не нужно ничего объяснять. Оно само проанализирует код, историю изменений и журнал Git, чтобы определить формат коммита и всю необходимую информацию. И создаст коммит, отправит его в правильную ветку.

## [09:48.220 → 09:52.660] dur=4.44s

**EN:** Again, we're not system prompting to do this. It just knows how to do this. The model is good.
**gemma:** Снова, мы не просим систему сделать это. Он просто знает, как это сделать. Модель хорошая.
**aya:** Опять же, система не требует от нас выполнения этих действий. Модель сама понимает, что нужно делать, и она хороша в этом.

## [09:55.920 → 10:02.380] dur=6.46s

**EN:** As you get a little bit more advanced, you're going to want to start to plug in your team's tools. And this is where Cloud Code starts to really shine.
**gemma:** Когда вы станете немного продвинутее, вам захочется начать подключать инструменты вашей команды. И вот здесь Cloud Code начинает по-настоящему сиять.
**aya:** По мере повышения вашей квалификации вы захотите интегрировать инструменты вашей команды. Именно здесь Cloud Code начинает ярко проявлять свои преимущества.

## [10:03.000 → 10:14.320] dur=11.32s

**EN:** And there's generally two kinds of tools. So one is batch tools. And an example of this, I just made up this, like, burly CLI. This isn't a real thing. But you can say use the CLI to do something. And you can tell Cloud Code about this.
**gemma:** В целом, существует два типа инструментов. Один — это пакетные инструменты. Я просто придумал пример, например, burly CLI. Это не существует в реальности. Но вы можете сказать, что используете CLI для чего-то. И вы можете рассказать об этом Cloud Code.
**aya:** Им могут быть два типа инструментов: пакетные и интерактивные. Например, вы можете использовать командную строку (CLI) для выполнения задач. Cloud Code может быть настроен для работы с такими инструментами.

## [10:14.580 → 10:18.520] dur=3.94s

**EN:** And you can tell it to use, for example, like dash dash help to figure out how to use it.
**gemma:** И вы можете сказать ему использовать, например, --help, чтобы узнать, как это использовать.
**aya:** И вы можете указать ему использовать команды типа `dash --help` для определения способов его использования.

## [10:18.780 → 10:26.680] dur=7.90s

**EN:** And this is efficient. If you find yourself using it a lot, you can also dump this into your Cloud MD, which we'll talk about in a bit, so Cloud can remember this across sessions.
**gemma:** Это эффективно. Если вы часто это используете, вы также можете добавить это в свой Cloud MD, о котором поговорим позже, чтобы Cloud запомнил это между сессиями.
**aya:** Это эффективно. Если вы часто используете такие инструменты, вы можете добавить их настройки в Cloud MD, чтобы Cloud запоминал их между сессиями.

## [10:27.040 → 10:29.180] dur=2.14s

**EN:** But this is a common pattern we follow at Anthropic.
**gemma:** Но это распространенный шаблон, который мы используем в Anthropic.
**aya:** Но это распространённая практика в Anthropic.

## [10:29.620 → 10:31.440] dur=1.82s

**EN:** And we see external customers used, too.
**gemma:** И мы видим, что это используют и внешние клиенты.
**aya:** И внешние клиенты также используют эту практику.

## [10:32.660 → 10:33.800] dur=1.14s

**EN:** And same thing with MCP.
**gemma:** И то же самое с MCP.
**aya:** То же самое касается и MCP.

## [10:34.580 → 10:43.360] dur=8.78s

**EN:** Cloud Code can use batch tools. It can use MCP tools. So, you know, just tell it about the tools. And you can add the MCP tool. And you can tell it how to use it. And it'll just start using it.
**gemma:** Cloud Code может использовать пакетные инструменты. Он может использовать инструменты MCP. То есть, вы просто рассказываете ему об инструментах, и можете добавить инструмент MCP. И вы можете сказать ему, как его использовать. И он просто начнет его использовать.
**aya:** Код облачных вычислений может использовать инструменты пакетной обработки. Он может использовать инструменты MCP. Итак, просто сообщите ему о наличии этих инструментов. Можно добавить инструмент MCP и указать, как им пользоваться. Тогда он начнёт их применять.

## [10:44.760 → 10:54.160] dur=9.40s

**EN:** And this is extremely powerful. Because when you start to use code on a new code base, you can just give it all of your tools, all the tools your team already uses for this code base.
**gemma:** И это очень мощно. Потому что когда вы начинаете использовать код в новой кодовой базе, вы можете просто передать ему все ваши инструменты, все инструменты, которые ваша команда уже использует для этой кодовой базы.
**aya:** Это чрезвычайно мощный инструмент. Потому что при начале работы с новым кодовой базой вы можете просто предоставить ему все инструменты, которые уже используются вашей командой для этой базы кода.

## [10:54.460 → 10:56.360] dur=1.90s

**EN:** And Cloud Code can use it on your behalf.
**gemma:** И Cloud Code может использовать это за вас.
**aya:** И Код Облачных Вычислений может использовать их от вашего имени.

## [11:01.980 → 11:03.400] dur=1.42s

**EN:** There's a few common workflows.
**gemma:** Есть несколько распространенных рабочих процессов.
**aya:** Существует несколько распространённых рабочих процессов.

## [11:04.760 → 11:13.320] dur=8.56s

**EN:** And this is the one that I talked about already. So kind of do a little bit of exploration. Do a little bit of planning. And ask me for confirmation before you start to write code.
**gemma:** И это то, о чем я уже говорил. То есть немного исследовать, немного спланировать и попросить меня подтвердить, прежде чем начать писать код.
**aya:** Это тот, о котором мы уже говорили. Так что проведём небольшое исследование, составим план и перед началом написания кода попросим вашего подтверждения.

## [11:13.960 → 11:16.240] dur=2.28s

**EN:** These other two on the right are extremely powerful.
**gemma:** Эти две справа очень мощные.
**aya:** Другие два на правом — чрезвычайно мощные инструменты.

## [11:17.060 → 11:24.940] dur=7.88s

**EN:** When Cloud has some way to check its work, so for example, by writing unit tests or screenshotting in Puppeteer or screenshotting the iOS simulator,
**gemma:** Когда Cloud может проверить свою работу, например, написав модульные тесты или сделав скриншоты в Puppeteer, или скриншоты из симулятора iOS,
**aya:** Когда Cloud имеет способ проверить свою работу, например, с помощью написания модульных тестов или скриншотов в Puppeteer или скриншотов симулятора iOS,

## [11:25.820 → 11:33.020] dur=7.20s

**EN:** then it can iterate. And this is incredible. Because if you give it, for example, a mock and you say build this web UI, it'll get pretty good.
**gemma:** Тогда он может итерировать. И это невероятно. Потому что если вы дадите ему, например, макет и скажете построить на его основе веб-интерфейс, он справится довольно хорошо.
**aya:** Тогда он может итеративно улучшаться. И это невероятно. Потому что если вы дадите ему мок и скажете создать этот веб-интерфейс, он станет довольно хорошим.

## [11:33.500 → 11:37.120] dur=3.62s

**EN:** But if you had to iterate two or three times, often it gets it almost perfect.
**gemma:** Но если ему нужно итерировать два или три раза, часто он добивается почти идеального результата.
**aya:** Но если вам нужно будет итеративно улучшать его два-три раза, часто он достигает почти идеального результата.

## [11:37.800 → 11:42.300] dur=4.50s

**EN:** So the trick is give it some sort of tool that it can use for feedback to check its work.
**gemma:** Так что хитрость в том, чтобы дать ему какой-то инструмент, который он мог бы использовать для обратной связи и проверки своей работы.
**aya:** Следовательно, секрет в том, чтобы предоставить ему инструмент, который может использовать для обратной связи и проверки своей работы.

## [11:42.620 → 11:46.120] dur=3.50s

**EN:** And then based on that, it will iterate by itself and you're going to get a much better result.
**gemma:** И затем, основываясь на этом, он будет итерировать сам, и вы получите гораздо лучший результат.
**aya:** И тогда, основываясь на этой обратной связи, он будет сам итеративно улучшаться, и вы получите гораздо лучший результат.

## [11:46.960 → 11:55.580] dur=8.62s

**EN:** So whatever your domain is, if it's unit tests or integration tests or screenshots for apps or web or anything, just give it a way to see its result. And it'll iterate and get a little bit better.
**gemma:** Так что какой бы ни был ваш домен — юнит-тесты, интеграционные тесты, скриншоты приложений или веб-страниц, или что-то другое — просто дайте ему возможность увидеть свой результат. И он будет итерировать, становясь немного лучше.
**aya:** Так что в любой области вашей работы — будь то модульные тесты, интеграционные тесты или скриншоты приложений или веб-сайтов — предоставьте ему способ видеть результат своей работы. И он будет итеративно улучшаться, становясь немного лучше.

## [12:00.290 → 12:04.590] dur=4.30s

**EN:** So these are the next steps. Teach Cloud how to use your tools and figure out the right workflow.
**gemma:** Итак, это следующие шаги. Научите Cloud пользоваться вашими инструментами и определите правильный рабочий процесс.
**aya:** Эти шаги включают обучение облачных систем использованию ваших инструментов и определение оптимального рабочего процесса.

## [12:05.010 → 12:13.610] dur=8.60s

**EN:** If you want Cloud to jump in a code, if you want it to brainstorm a little bit, make a plan, if you want it to iterate, kind of have some sense of that. So you know how to prompt Cloud to do what you want.
**gemma:** Если вы хотите, чтобы Cloud вписался в код, чтобы он немного набросал идеи, составил план или итерировал, вы должны знать, как промтить Cloud, чтобы он сделал то, что вам нужно.
**aya:** Чтобы Cloud эффективно работал с кодом, генерировал идеи, разрабатывал планы и итеративно улучшал результаты, необходимо правильно формулировать запросы. Знайте, как дать Cloud понять, что именно от него требуется.

## [12:17.350 → 12:21.430] dur=4.08s

**EN:** As you go deeper, beyond tools, you want to start to give Cloud more context.
**gemma:** По мере углубления, вы должны начать давать Cloud больше контекста, выходя за рамки инструментов.
**aya:** По мере углубления работы, выходя за рамки инструментов, важно предоставлять Cloud дополнительный контекст для более точного и качественного выполнения задач.

## [12:21.910 → 12:32.930] dur=11.02s

**EN:** And the more context, the smarter the decisions will be. Because as an engineer working in a code base, you have a ton of context in your head about your systems and all the history and everything else. So there's different ways to give this to Cloud.
**gemma:** Чем больше контекста, тем умнее будут решения. Потому что как инженер, работающий с кодовой базой, вы храните в голове массу контекста о своих системах, всей истории и прочее. Поэтому есть разные способы передать это Cloud.
**aya:** Чем больше контекста вы предоставляете Cloud, тем умнее и точнее будут его решения. Как инженер, работающий с кодовой базой, у вас в голове накоплен огромный опыт и знания о системах, их истории и других аспектах. Существует несколько способов передачи этого контекста Cloud.

## [12:33.310 → 12:35.370] dur=2.06s

**EN:** And as you give Cloud more context, it'll do better.
**gemma:** И чем больше контекста вы дадите Cloud, тем лучше он справится.
**aya:** Предоставляя Cloud больше контекста, вы помогаете ему принимать более обоснованные и качественные решения.

## [12:37.190 → 12:41.150] dur=3.96s

**EN:** There's different ways to do this. The simplest one is what we call CloudMD.
**gemma:** Есть разные способы это сделать. Самый простой — это то, что мы называем CloudMD.
**aya:** Существует различные способы передачи контекста. Один из самых простых — это метод CloudMD.

## [12:41.670 → 12:44.050] dur=2.38s

**EN:** And Cloud.MD is the special file name.
**gemma:** И Cloud.MD — это специальное имя файла.
**aya:** Cloud.MD — это специальный файл, используемый для передачи контекстной информации об облачных системах.

## [12:44.830 → 12:49.530] dur=4.70s

**EN:** The simplest place to put it is in the project root. So the same directory you start Cloud in,
**gemma:** Самое простое место для него — корневая папка проекта. То есть та же директория, где вы запускаете Cloud,
**aya:** Самый простой способ разместить файл Cloud.MD — в корневой директории проекта, то есть той же директории, из которой вы запускаете Cloud.

## [12:50.210 → 12:54.650] dur=4.44s

**EN:** put a CloudMD in there. And that'll get automatically read into context at the start of every session.
**gemma:** положите туда CloudMD. И он автоматически будет загружен в контекст в начале каждой сессии.
**aya:** Создайте файл Cloud.MD в корневой директории проекта, и он будет автоматически считываться как контекст при каждом запуске сессии.

## [12:55.190 → 12:57.710] dur=2.52s

**EN:** And essentially, the first user turn will include the CloudMD.
**gemma:** По сути, первый ход пользователя будет включать CloudMD.
**aya:** Первый шаг пользователя будет включать загрузку и обработку файла Cloud.MD, что обеспечит необходимый контекст для дальнейшего взаимодействия.

## [12:59.590 → 13:01.790] dur=2.20s

**EN:** You can also have a local CloudMD.
**gemma:** Вы также можете использовать локальный CloudMD.
**aya:** Также можно иметь локальную версию файла Cloud.MD, которая будет использоваться в качестве начального контекста при работе с облачным интерфейсом.

## [13:02.150 → 13:07.490] dur=5.34s

**EN:** And this one, you don't usually check into source control. So CloudMD, you should check into source control,
**gemma:** И этот CloudMD обычно не добавляют в систему контроля версий. Поэтому CloudMD нужно добавить.
**aya:** Файл Cloud.MD, как правило, не добавляется в систему контроля версий, но для обеспечения безопасности и совместной работы его рекомендуется хранить в репозитории вместе с кодом проекта.

## [13:07.930 → 13:10.770] dur=2.84s

**EN:** share with your team so that you can write it once and share it with your team.
**gemma:** Поделитесь этим с командой, чтобы написать его один раз и передать всем.
**aya:** Делитесь файлом Cloud.MD со своей командой, чтобы избежать дублирования усилий и обеспечить единообразие в работе.

## [13:11.610 → 13:19.270] dur=7.66s

**EN:** This one, you don't check in. It's just for you. The kinds of things you put in CloudMD, it's like common bash commands, common MCP tools,
**gemma:** Этот не добавляют. Он только для вас. Типа вещей, которые вы вносите в CloudMD — это общие команды bash, общие инструменты MCP.
**aya:** Этот файл не добавляется в систему контроля версий, он предназначен исключительно для вашего использования. В нем можно хранить общие командные строки, инструменты и конфигурации, которые часто используются.

## [13:19.850 → 13:21.490] dur=1.64s

**EN:** architectural decisions,
**gemma:** Архитектурные решения,
**aya:** архитектурные решения,

## [13:22.010 → 13:26.550] dur=4.54s

**EN:** important files, anything that you would kind of typically need to know in order to work in this code base.
**gemma:** Важные файлы, всё, что вам обычно нужно знать, чтобы работать с этой кодовой базой.
**aya:** важные файлы и информация, необходимая для эффективной работы с этим кодом.

## [13:27.030 → 13:31.050] dur=4.02s

**EN:** Try to keep it pretty short, because if it gets too long, it's just going to use up a bunch of context.
**gemma:** Постарайтесь сделать это коротким, потому что если будет слишком длинным, это займёт много контекста.
**aya:** Конечно, краткость — сестра таланта. Включите ключевые файлы, инструменты и документацию, необходимые для быстрого понимания и работы с кодом.

## [13:31.410 → 13:32.690] dur=1.28s

**EN:** And it's usually not that useful.
**gemma:** И это обычно не очень полезно.
**aya:** В большинстве случаев это неэффективно. Сосредоточьтесь на важном и актуальном, чтобы сэкономить время и усилия.

## [13:33.210 → 13:34.550] dur=1.34s

**EN:** So just try to keep it as short as you can.
**gemma:** Поэтому просто постарайтесь сделать это максимально коротким.
**aya:** Файлы: основные скрипты, конфигурации, документация. Инструменты: IDE, версии контроля. Дополнительно: инструкции по запуску, требования к системе.

## [13:35.190 → 13:42.590] dur=7.40s

**EN:** And for example, in our code base, we have common bash commands, we have a style guide, we have a few core files, kind of things like that.
**gemma:** Например, в нашей кодовой базе есть общие команды bash, руководство по стилю, несколько основных файлов и тому подобное.
**aya:** В нашей базе кода есть общие командные файлы (bash), стиль руководства, основные файлы и другие важные ресурсы.

## [13:43.610 → 13:46.290] dur=2.68s

**EN:** All the other CloudMDs, you can put them in other nested child
**gemma:** Все остальные CloudMD можно поместить в другие вложенные дочерние элементы.
**aya:** Все остальные CloudMD-файлы можно разместить в других подкаталогах.

## [13:46.990 → 13:48.930] dur=1.94s

**EN:** directories, and Cloud will pull them in on demand.
**gemma:** каталоги, и Cloud подтянет их по мере необходимости.
**aya:** Директории с файлами будут загружаться в облако по требованию.

## [13:50.430 → 13:53.070] dur=2.64s

**EN:** So these are the CloudMDs that will get pulled in automatically.
**gemma:** Таким образом, эти CloudMD будут подгружаться автоматически.
**aya:** Это CloudMD-файлы, которые будут автоматически загружаться.

## [13:53.870 → 14:00.930] dur=7.06s

**EN:** But then also, you can put CloudMDs in nested directories, and those will get put, those will get automatically pulled when Cloud works in those directories.
**gemma:** Но вы также можете поместить CloudMD в вложенные каталоги, и они будут автоматически подгружаться, когда Cloud будет работать в этих каталогах.
**aya:** Также можно размещать CloudMD-файлы в подкаталогах, и они будут автоматически загружаться при работе облака в этих каталогах.

## [14:03.090 → 14:13.210] dur=10.12s

**EN:** And of course, if you're, you know, a company, maybe you want a CloudMD that's shared across all the different code bases, and you want to manage it on behalf of your users, and you can put it in your enterprise route, and that'll get pulled in automatically.
**gemma:** И, конечно, если вы компания, возможно, вам нужен CloudMD, общий для всех кодовых баз, и вы хотите управлять им от имени пользователей. Вы можете поместить его в свой корпоративный маршрут, и он будет автоматически подгружен.
**aya:** И, конечно, если вы компания, возможно, вам нужен общий CloudMD для всех проектов с кодом, который нужно управлять от имени пользователей. Его можно разместить в корпоративном хранилище, и он будет автоматически загружаться для всех сотрудников.

## [14:17.300 → 14:23.780] dur=6.48s

**EN:** There's a ton of ways to pull in context. I actually had a lot of trouble putting this slide together just to communicate the breadth of ways you can do this.
**gemma:** Существует множество способов подгрузить контекст. Мне было очень трудно собрать этот слайд, чтобы передать всю широту возможностей.
**aya:** Существует множество способов загрузки контекста. Я сам столкнулся с трудностями при создании этого слайда, чтобы показать разнообразие подходов.

## [14:24.540 → 14:26.120] dur=1.58s

**EN:** But CloudMD is pulled in automatically.
**gemma:** Но CloudMD подгружается автоматически.
**aya:** CloudMD загружается автоматически.

## [14:26.840 → 14:34.660] dur=7.82s

**EN:** You can also use slash commands. So this is .cloud slash commands, and this can be in your home directory, or it can be checked into your project. And this is for slash commands.
**gemma:** Вы также можете использовать слеш-команды. Вот .cloud slash commands, и это может находиться в вашей домашней директории или быть включено в ваш проект. А это для slash commands.
**aya:** Также можно использовать командные строки. Например, `.cloud/commands` — это может быть в домашнем каталоге или включено в проект. Это для командных строк.

## [14:35.440 → 14:42.340] dur=6.90s

**EN:** And over here, we have a few examples of the slash commands that we have in Cloud code itself.
**gemma:** А здесь у нас несколько примеров слеш-команд, которые есть в самом Cloud Code.
**aya:** И здесь приведены несколько примеров команд строки, встроенных в сам код Cloud.

## [14:43.220 → 14:50.940] dur=7.72s

**EN:** And so, for example, if you're in the Cloud code repo, and you see issues getting labeled, that's actually this workflow running here. It's labeled GitHub issues.
**gemma:** Например, если вы находитесь в репозитории Cloud Code и видите, что проблемы получают метки, это на самом деле работа этого рабочего процесса. Это метки GitHub Issues.
**aya:** Например, если вы находитесь в репозитории кода Cloud и видите, как задачи автоматически получают метки, это работает благодаря этому рабочему процессу, который использует метки GitHub для задач.

## [14:51.800 → 15:03.220] dur=11.42s

**EN:** And we have a GitHub action running, the same one we talked about this morning, where Cloud code will run this command, and it's just a slash command. It'll run, and it'll label the issues so humans don't have to. It just saves us a bunch of time.
**gemma:** У нас запущен GitHub Action, тот же, о котором мы говорили сегодня утром. Cloud Code выполнит эту команду, и это просто слеш-команда. Она запустится и пометит проблемы, чтобы людям не пришлось этого делать. Это просто экономит нам кучу времени.
**aya:** И у нас работает действие GitHub, о котором мы говорили сегодня утром: код Cloud выполняет эту команду, которая является просто командной строкой. Оно автоматически меткирует задачи, экономя нам много времени.

## [15:04.620 → 15:07.260] dur=2.64s

**EN:** And of course, you can add mention files to pull them into context.
**gemma:** И, конечно, вы можете добавить файлы упоминаний, чтобы включить их в контекст.
**aya:** Конечно, вы можете добавлять ссылки на файлы, чтобы включить их в контекст.

## [15:08.060 → 15:09.240] dur=1.18s

**EN:** And like I said before,
**gemma:** Как я уже говорил,
**aya:** Как я уже говорил ранее,

## [15:09.940 → 15:13.240] dur=3.30s

**EN:** QuadMDs in a nested directory get pulled in when Quad works in that directory.
**gemma:** QuadMD в вложенной директории подтягиваются, когда Quad работает в этой директории.
**aya:** КвадMDs из вложенных каталогов автоматически включаются, когда Quad работает в этом каталоге.

## [15:18.160 → 15:19.620] dur=1.46s

**EN:** So give Quad more context.
**gemma:** Таким образом, вы даете Quad больше контекста.
**aya:** Таким образом, предоставьте Quad больше контекста.

## [15:20.380 → 15:24.260] dur=3.88s

**EN:** And it's definitely worth taking the time to tune context. You can run it through a prompt improver.
**gemma:** И определенно стоит потратить время на настройку контекста. Вы можете пропустить его через улучшитель промптов.
**aya:** И действительно, стоит уделить время настройке контекста. Вы можете запустить его через улучшитель запросов.

## [15:24.580 → 15:32.380] dur=7.80s

**EN:** Consider who the context is for. If you want to pull it in every time, if you want to pull it in on demand, if you want to share it with a team, if it's a personal preference,
**gemma:** Подумайте, для кого предназначен контекст. Хотите ли вы, чтобы он подтягивался всегда, по требованию, чтобы поделиться им с командой или это личное предпочтение.
**aya:** Учитывайте, для кого предназначен контекст. Если вы хотите включать его автоматически при каждом запуске, по требованию, делиться с командой или это личная настройка — всё это влияет на выбор подхода.

## [15:32.800 → 15:37.100] dur=4.30s

**EN:** definitely take the time to tune it. This will improve performance dramatically if you do it right.
**gemma:** Обязательно уделите время его настройке. Если сделать это правильно, это значительно улучшит производительность.
**aya:** Безусловно, уделите время настройке контекста. Это значительно улучшит производительность, если сделать это правильно.

## [15:41.730 → 15:42.850] dur=1.12s

**EN:** As you get more advanced,
**gemma:** По мере того, как вы становитесь более опытным,
**aya:** По мере вашего продвижения вперед...

## [15:43.310 → 15:48.110] dur=4.80s

**EN:** you're going to want to think about this a little bit more, this kind of hierarchy of different ways to pull in everything.
**gemma:** Вам захочется задуматься об этом немного больше — о такой иерархии различных способов подтягивания всего.
**aya:** По мере развития вы будете хотеть более тщательно задуматься о такой иерархии различных способов включения информации.

## [15:48.410 → 15:56.110] dur=7.70s

**EN:** So like not just QuadMD, but also config and kind of everything about Quad you can pull in in this hierarchical way.
**gemma:** То есть не только QuadMD, но и конфигурация, и всё, что касается Quad, которое можно подтянуть таким иерархическим способом.
**aya:** Так что не только QuadMD, но и конфигурация, а также все аспекты Quad, которые можно включить в иерархическом порядке.

## [15:56.530 → 16:02.090] dur=5.56s

**EN:** So projects are specific to your Git repo, and this you can check in, or you can make it just for you.
**gemma:** Проекты привязаны к вашему репозиторию Git, и вы можете это проверить, или сделать это только для себя.
**aya:** Проекты специфичны для вашего репозитория Git, и вы можете проверять их или создавать только для себя.

## [16:02.630 → 16:07.290] dur=4.66s

**EN:** You can also have global configs that are across all your projects, or you can have enterprise policies.
**gemma:** Вы также можете иметь глобальные конфигурации для всех проектов или корпоративные политики.
**aya:** Вы также можете иметь глобальные конфигурации, действующие по всем проектам, или корпоративные политики.

## [16:07.690 → 16:12.030] dur=4.34s

**EN:** And this is essentially a global config that you roll out for all of your employees, everyone on your team automatically.
**gemma:** Это, по сути, глобальная конфигурация, которую вы разворачиваете для всех сотрудников, для всей вашей команды автоматически.
**aya:** И это по сути глобальная конфигурация, которую вы внедряете для всех сотрудников, для каждого члена команды автоматически.

## [16:14.130 → 16:21.230] dur=7.10s

**EN:** And this slide is like pretty information dense, but the point is this applies to a lot of stuff. So you can do this for splash commands, you can do it for permissions.
**gemma:** И этот слайд очень насыщен информацией, но главное, что это применимо ко многим вещам. Вы можете сделать это для команд запуска, вы можете сделать это для разрешений.
**aya:** И эта слайд очень информативна, но основная идея в том, что это применимо к многим вещам. Вы можете использовать это для команд приветствия, а также для управления разрешениями.

## [16:21.550 → 16:25.250] dur=3.70s

**EN:** So for example, if you have a bash command that you would run for all your employees,
**gemma:** Например, если у вас есть команда bash, которую вы хотите запустить для всех сотрудников,
**aya:** Например, если у вас есть команда Bash, которую вы запускаете для всех сотрудников...

## [16:25.790 → 16:32.170] dur=6.38s

**EN:** like all your employees use this like test command, for example, you can actually just check it into this enterprise policies file.
**gemma:** Например, если все ваши сотрудники используют эту тестовую команду, вы можете просто добавить ее в файл корпоративных политик.
**aya:** ...такие как команда тестирования, вы можете просто добавить её в файл корпоративных политик.

## [16:32.630 → 16:36.850] dur=4.22s

**EN:** And then any employee, when they run this command, it will be auto approved, which is pretty convenient.
**gemma:** И тогда любой сотрудник, запустив эту команду, получит автоматическое одобрение, что очень удобно.
**aya:** И тогда любому сотруднику, выполняющему эту команду, будет автоматически одобрено действие, что очень удобно.

## [16:37.430 → 16:39.170] dur=1.74s

**EN:** And you can also use this to block commands.
**gemma:** И вы также можете использовать это, чтобы заблокировать команды.
**aya:** Также можно использовать это для блокировки команд.

## [16:39.550 → 16:49.270] dur=9.72s

**EN:** So for example, let's say there's a URL that should never be fetched, just add it to this config, and that will make it so an employee cannot override it, and that URL can never be fetched.
**gemma:** Например, если есть URL, который никогда не должен загружаться, просто добавьте его в эту конфигурацию, и сотрудник не сможет его обойти, а URL никогда не будет загружен.
**aya:** Например, если есть URL-адрес, который никогда не должен загружаться, добавьте его в конфигурацию — это предотвратит попытку сотрудника обойти ограничение и гарантирует, что этот URL-адрес никогда не будет загружен.

## [16:49.670 → 16:53.170] dur=3.50s

**EN:** So pretty convenient, both to unblock people and also just to keep your code base safe.
**gemma:** Так довольно удобно — и для разблокировки пользователей, и для защиты кодовой базы.
**aya:** Очень удобно как для разблокировки людей, так и для защиты кода от нежелательных действий.

## [16:54.730 → 16:56.190] dur=1.46s

**EN:** And then same thing for MCP servers,
**gemma:** И то же самое для серверов MCP.
**aya:** И то же самое касается серверов MCP — настройка блокировок и ограничений обеспечивает безопасность и контроль над доступом.

## [16:56.690 → 17:04.690] dur=8.00s

**EN:** have an MCP JSON file, check it into the code base, that way any time someone runs quad code in your code base, they'll be prompted to install the MCP servers, and share
**gemma:** Создайте JSON-файл для MCP, добавьте его в кодовую базу. Таким образом, каждый раз, когда кто-то запускает код в вашей базе, ему будет предложено установить серверы MCP и поделиться.
**aya:** Создайте JSON-файл для MCP, включите его в кодовую базу. При запуске кода пользователи будут автоматически приглашены к установке и обмену серверами MCP.

## [17:04.690 → 17:12.720] dur=8.03s

**EN:** it with the team. If you're not sure which of these to use, this is like a kind of an insane
**gemma:** с командой. Если вы не уверены, какой из них использовать, это похоже на какой-то безумный
**aya:** Если вы не уверены, какой инструмент выбрать, рассмотрите все варианты как набор эффективных решений для работы команды. Выбор зависит от конкретных задач и предпочтений.

## [17:12.720 → 17:22.780] dur=10.06s

**EN:** matrix, because we support a lot of stuff, and engineer workflows are very flexible, and every company is different, so we kind of want to support everything. So if you're not sure how to get started, I would recommend start with shared project context.
**gemma:** по матрице, потому что мы поддерживаем много всего, и рабочие процессы инженеров очень гибкие, и каждая компания разная, поэтому мы хотим поддерживать всё. Так что, если вы не знаете, с чего начать, я бы посоветовал начать с общего контекста проекта.
**aya:** Поскольку ваша команда поддерживает множество инструментов и имеет гибкие рабочие процессы, рекомендуется начать с создания общего контекста проекта. Это позволит обеспечить согласованность и совместную работу над различными задачами, адаптируя инструменты под уникальные потребности компании.

## [17:24.140 → 17:30.740] dur=6.60s

**EN:** You write this once, and then you share it with everyone on the team, and you get this kind of network effect where, you know, someone does a little bit of work, and everyone on the team benefits.
**gemma:** Вы пишете это один раз, а затем делитесь этим со всей командой, и вы получаете такой сетевой эффект, когда кто-то делает небольшую работу, и от этого выигрывает вся команда.
**aya:** Создавая общий контекст проекта и делая его доступным для всей команды, вы запускаете сетевой эффект. Каждое внесённое изменение приносит пользу всем участникам, стимулируя совместную работу и повышая эффективность.

## [17:34.700 → 17:37.140] dur=2.44s

**EN:** There's a lot of tools built into quad to manage this.
**gemma:** В Quad есть много инструментов для управления этим.
**aya:** В Quad есть множество встроенных инструментов для управления этими процессами.

## [17:37.680 → 17:42.760] dur=5.08s

**EN:** So as an example, if you run slash memory, you can see all the different memory files that are getting pulled in.
**gemma:** Например, если вы запустите команду slash memory, вы увидите все различные файлы памяти, которые подтягиваются.
**aya:** Например, используя функцию мониторинга памяти, вы можете просматривать все файлы памяти, загружаемые системой.

## [17:43.140 → 17:47.400] dur=4.26s

**EN:** So maybe I have an enterprise policy, I have my user memory, I have project quad MD,
**gemma:** У меня может быть корпоративная политика, моя пользовательская память, проект Quad MD,
**aya:** В вашей корпоративной политике могут быть определены правила использования памяти, индивидуальные настройки для пользователей и проектные параметры Quad MD.

## [17:47.920 → 17:51.660] dur=3.74s

**EN:** and then maybe there's a nested quad MD. That's only pulled in for certain directories.
**gemma:** И, возможно, вложенный Quad MD. Он подтягивается только для определенных каталогов.
**aya:** И в случае вложенного проекта Quad MD, он загружается только для определенных каталогов.

## [17:53.830 → 18:01.170] dur=7.34s

**EN:** And then similarly, when you do slash memory, you can edit particular memory files. When you type pound sign to remember something, you can pick which memory you wanted to go to.
**gemma:** И аналогично, когда вы делаете slash memory, вы можете редактировать определенные файлы памяти. Когда вы вводите решетку, чтобы что-то запомнить, вы можете выбрать, к какой памяти вы хотите перейти.
**aya:** Аналогично, используя команду /память, вы можете редактировать конкретные файлы памяти. При вводе символа # для запоминания, вы выбираете нужную память, к которой хотите перейти.

## [18:06.100 → 18:09.920] dur=3.82s

**EN:** So yeah, that's the next step. Take the time to configure quad MD,
**gemma:** Итак, да, это следующий шаг. Уделите время настройке Quad MD,
**aya:** Следующим шагом будет настройка проекта Quad MD, чтобы он соответствовал вашим требованиям.

## [18:10.360 → 18:16.160] dur=5.80s

**EN:** MCP servers, all the stuff that your team uses so that you can use it once, configure it once, and then share it with everyone.
**gemma:** Серверы MCP, все, что использует ваша команда, чтобы вы могли настроить это один раз и поделиться со всеми.
**aya:** Серверы MCP — это инструменты, которые ваша команда использует для единовременной настройки и совместного доступа к конфигурациям.

## [18:19.040 → 18:21.760] dur=2.72s

**EN:** An example of this is in our apps repo.
**gemma:** Пример этого — в нашем репозитории приложений.
**aya:** Примером этого является наше приложение в репозитории кода.

## [18:22.620 → 18:30.220] dur=7.60s

**EN:** For Anthropic, this is like the repo that we have all of our web and apps code in. There's a Puppeteer MCP server, and we share this with the team.
**gemma:** Для Anthropic это как репозиторий, где хранится весь наш код для веба и приложений. Там есть сервер MCP Puppeteer, и мы делимся им с командой.
**aya:** Для компании Anthropic это аналогично общему репозиторию с кодом веб-приложений и мобильных приложений. У нас есть сервер MCP с использованием Puppeteer, который мы делимся со всей командой.

## [18:30.980 → 18:40.760] dur=9.78s

**EN:** And there's an MCP JSON checked in, so any engineer working in that repo can use Puppeteer in order to pilot end-to-end tests and to screenshot automatically and iterate so that every engineer doesn't have to install it themselves.
**gemma:** И там есть MCP JSON, который позволяет любому инженеру в этом репозитории использовать Puppeteer для пилотирования сквозных тестов, автоматического создания скриншотов и итераций, чтобы не каждый инженер должен был устанавливать его самостоятельно.
**aya:** И есть конфигурированный в виде JSON сервер MCP, что позволяет любому инженеру, работающему с этим репозиторием, использовать Puppeteer для выполнения тестов на конечных узлах и автоматического создания скриншотов, не устанавливая его самостоятельно.

## [18:45.930 → 18:57.350] dur=11.42s

**EN:** This is a talk about pro tips. I just want to take a quick interlude to talk about some common key bindings that people may not know. It's very hard to build for terminal. It's also very fun. It feels like rediscovering this new design language.
**gemma:** Это рассказ о полезных советах. Я просто хочу сделать небольшую паузу, чтобы поговорить о некоторых сочетаниях клавиш, о которых люди могут не знать. Это очень сложно реализовать в терминале. Но это и очень весело. Это похоже на повторное открытие нового языка дизайна.
**aya:** Это разговор о профессиональных советах. Я хочу сделать небольшую паузу, чтобы рассказать о распространённых сочетаниях клавиш, которые многие могут не знать. Создание для терминала — сложная задача, но это также очень увлекательно. Это как переосмысление нового языка дизайна.

## [18:57.950 → 19:00.390] dur=2.44s

**EN:** But something about terminals, it's extremely minimal.
**gemma:** Но что касается терминалов, они чрезвычайно минималистичны.
**aya:** Но терминалы по своей природе чрезвычайно минималистичны.

## [19:01.090 → 19:05.690] dur=4.60s

**EN:** And so sometimes it's hard to discover these key bindings. And here's just a quick reference sheet.
**gemma:** И поэтому иногда трудно обнаружить эти сочетания клавиш. Вот просто справочная таблица.
**aya:** И поэтому иногда сложно запомнить эти сочетания клавиш. Вот краткое справочное руководство.

## [19:06.010 → 19:08.850] dur=2.84s

**EN:** So any time, you can hit shift tab to accept edits.
**gemma:** Так что в любое время вы можете нажать Shift+Tab, чтобы принять правки.
**aya:** В любой момент вы можете нажать Shift + Tab для подтверждения изменений.

## [19:09.810 → 19:16.510] dur=6.70s

**EN:** And this switches you into auto accept edits mode. So bash commands still need approval, but edits are auto accepted. And you can always ask Claude to undo them later.
**gemma:** Это переключает вас в режим автоматического принятия правок. Команды bash всё ещё требуют одобрения, но правки принимаются автоматически. А позже вы всегда можете попросить Клода отменить их.
**aya:** Это переключает вас в режим автоматического принятия изменений. Команды Bash по-прежнему требуют подтверждения, но изменения принимаются автоматически. Вы всегда можете попросить Клауда отменить их позже.

## [19:18.150 → 19:26.350] dur=8.20s

**EN:** For example, I'll do this if I know Claude's on the right track or if it's writing unit tests and iterating on tests, I'll usually just switch into auto accept mode so I don't have to okay every single
**gemma:** Например, я сделаю это, если знаю, что Клод на верном пути, или если он пишет юнит-тесты и итерирует над ними. Обычно я просто переключаюсь в режим автоматического принятия, чтобы не одобрять каждую
**aya:** Например, я буду делать это, если знаю, что Клод движется в правильном направлении, или если речь идёт о написании модульных тестов и итерации над ними — обычно я переключаюсь в режим автоматического принятия изменений, чтобы не подтверждать каждый отдельный шаг.

## [19:26.350 → 19:37.440] dur=11.09s

**EN:** edit. Any time you want Claude to remember something, so for example, if it's not using a tool correctly and you want it to use it correctly from then on, just type the pound sign and then tell it what to remember.
**gemma:** В любое время, когда вы хотите, чтобы Клод что-то запомнил. Например, если он неправильно использует инструмент, и вы хотите, чтобы он использовал его правильно в дальнейшем, просто введите решетку и скажите ему, что запомнить.
**aya:** Редактируйте. Каждый раз, когда вы хотите, чтобы Клод запомнил что-то, например, если он неправильно использует инструмент и вам нужно, чтобы он использовал его правильно в дальнейшем, просто введите символ "#" и укажите, что нужно запомнить.

## [19:37.780 → 19:40.220] dur=2.44s

**EN:** And it'll remember it. It'll incorporate it into Claude MD automatically.
**gemma:** И он это запомнит. Он автоматически включит это в Claude MD.
**aya:** И он запомнит это. Это автоматически будет включено в базу знаний Клауда MD.

## [19:42.040 → 19:50.200] dur=8.16s

**EN:** If you ever want to drop down to bash mode, so just run a bash command, you can hit the exclamation mark and type in your command. That'll run locally, but that also goes into the context window.
**gemma:** Если вам когда-нибудь понадобится перейти в режим bash, просто выполните команду bash. Вы можете нажать восклицательный знак и ввести свою команду. Она выполнится локально, но также попадет в контекстное окно.
**aya:** Если вам нужно переключиться на режим Bash, просто введите "!" и команду, которая будет выполнена локально и добавлена в контекстное окно.

## [19:50.820 → 19:52.780] dur=1.96s

**EN:** So Claude will see it on the next turn.
**gemma:** Так что Клод увидит это в следующем ходе.
**aya:** Клауд увидит это на следующем ходу.

## [19:53.720 → 20:00.800] dur=7.08s

**EN:** And this is pretty good for long running commands if you know exactly what you want to do or any command that you want to get into context. And Claude will see the command and the output.
**gemma:** И это очень хорошо для длительных команд, если вы точно знаете, что хотите сделать, или для любой команды, которую хотите включить в контекст. И Клод увидит команду и вывод.
**aya:** Это отлично подходит для длинных команд, если вы точно знаете, что хотите сделать, или для любой команды, которую вы хотите добавить в контекст. Клауд увидит команду и её вывод.

## [20:02.990 → 20:04.650] dur=1.66s

**EN:** You can add mention thousand folders.
**gemma:** Вы можете добавить упоминание тысячи папок.
**aya:** Можно упомянуть тысячи папок.

## [20:05.250 → 20:07.990] dur=2.74s

**EN:** Any time, you can hit escape to stop what Claude is doing.
**gemma:** В любое время вы можете нажать Escape, чтобы остановить то, что делает Клод.
**aya:** В любое время вы можете нажать Esc, чтобы остановить то, что делает Клауд.

## [20:08.470 → 20:10.730] dur=2.26s

**EN:** No matter what Claude is doing, you can always safely hit escape.
**gemma:** Что бы ни делал Клод, вы всегда можете безопасно нажать Escape.
**aya:** Независимо от того, чем занимается Клауд, вы всегда можете безопасно нажать Esc.

## [20:11.150 → 20:13.430] dur=2.28s

**EN:** It's not going to corrupt the session. It's not going to mess anything up.
**gemma:** Это не повредит сессию. Ничего не испортит.
**aya:** Это не повредит сессию и не испортит что-либо.

## [20:13.950 → 20:17.310] dur=3.36s

**EN:** So maybe Claude is doing a file edit. I'll hit escape. I'll tell it what to do differently.
**gemma:** Может быть, Клод редактирует файл. Я нажму Escape и скажу ему, как это сделать по-другому.
**aya:** Так как Клауд может редактировать файл, нажмите Esc, чтобы изменить его действия.

## [20:17.750 → 20:26.310] dur=8.56s

**EN:** Or maybe it suggested a 20 line edit. And I'm like, actually, 19 of these lines look perfect, but one line you should change. I'll hit escape. I'll tell it that. And then I'll tell it to redo the edit.
**gemma:** Или, может быть, он предложил правку из 20 строк. И я скажу: «На самом деле, 19 из этих строк идеальны, но одну нужно изменить». Я нажму Escape и сообщу ему об этом, а затем попрошу переделать правку.
**aya:** Или предположим, что программа предложила внести изменения в 20 строк кода, но 19 из них идеальны, и вам нужно изменить только одну. Нажмите Esc, чтобы изменить команду, а затем повторите команду с указанием изменить именно одну строку и применить изменения.

## [20:28.940 → 20:31.180] dur=2.24s

**EN:** You can hit escape twice to jump back in history.
**gemma:** Вы можете нажать Escape дважды, чтобы вернуться в историю.
**aya:** Двойное нажатие Esc позволяет вернуться в предыдущую версию редактирования.

## [20:31.820 → 20:38.120] dur=6.30s

**EN:** And then after you're done with the session, you can start Claude with a resume to resume that session if you want or dash dash continue.
**gemma:** И после завершения сеанса вы можете запустить Клода с командой resume, чтобы продолжить сеанс, или использовать — continue.
**aya:** После завершения сессии вы можете запустить Клауда с опцией "продолжить" для возобновления работы или "начать заново" для нового сеанса.

## [20:39.860 → 20:47.060] dur=7.20s

**EN:** And then any time if you want to see more output, hit control R. And that'll show you the entire output, the same thing that Claude sees in its context window.
**gemma:** И если вы захотите увидеть больше вывода, нажмите Control + R. Это покажет вам весь вывод, то же, что видит Клод в своем контекстном окне.
**aya:** Для просмотра полного вывода (то же, что и в контекстном окне Клауда) нажмите Ctrl+R в любое время.

## [20:53.260 → 20:57.560] dur=4.30s

**EN:** The next thing I want to talk about is the Claude code SDK. So we talked about this at the top.
**gemma:** Дальше я хочу поговорить о Claude Code SDK. Мы уже затронули это в начале.
**aya:** Далее я хочу обсудить SDK Клауда. Мы уже упоминали это ранее.

## [20:57.980 → 21:03.400] dur=5.42s

**EN:** Right after this, Sid is doing a session, I think, just across the hallway. And he's going to go super deep on the SDK.
**gemma:** Сразу после этого Сид проводит сессию, я думаю, через коридор. И он очень подробно расскажет об SDK.
**aya:** Сразу после этого Сид проводит сессию по SDK, наверное, прямо напротив. Он углубится в его изучение.

## [21:03.900 → 21:09.580] dur=5.68s

**EN:** If you hadn't played around with this, if you use the dash P flag in Claude, this is what the SDK is.
**gemma:** Если вы не играли с этим, если используете флаг —P в Claude, то это и есть SDK.
**aya:** Если бы вы не экспериментировали с этим, используя флаг dash P в Клауде, это было бы SDK.

## [21:09.920 → 21:13.380] dur=3.46s

**EN:** And we've been landing a bunch of features over the last few weeks to make it even better.
**gemma:** И за последние несколько недель мы добавили много функций, чтобы сделать его еще лучше.
**aya:** За последние несколько недель мы внедрили множество функций, чтобы сделать его ещё лучше.

## [21:15.140 → 21:21.000] dur=5.86s

**EN:** So yeah, you can build on top of this. You can do cool stuff. This is exactly the thing that Claude code uses. It's exactly the same SDK.
**gemma:** Так что да, вы можете строить на этом. Вы можете делать крутые вещи. Это именно то, что использует код Claude. Это тот же SDK.
**aya:** Да, вы можете строить на этом. Вы можете делать крутые вещи. Это именно то, что использует код Клауда. То же самое SDK.

## [21:22.500 → 21:26.980] dur=4.48s

**EN:** And so, for example, something you can do is Claude dash P. So this is the CLI SDK.
**gemma:** И, например, то, что вы можете сделать, это Claude dash P. Это CLI SDK.
**aya:** И так, например, вы можете сделать Claude dash P. Это CLI SDK.

## [21:27.360 → 21:29.100] dur=1.74s

**EN:** You can pass a prompt.
**gemma:** Вы можете передать запрос.
**aya:** Вы можете передать подсказку.

## [21:29.760 → 21:33.380] dur=3.62s

**EN:** You can pass some allowed tools, which could include specific batch commands.
**gemma:** Вы можете передать разрешенные инструменты, которые могут включать конкретные пакетные команды.
**aya:** Вы можете передать некоторые разрешённые инструменты, которые могут включать конкретные команды батча.

## [21:33.780 → 21:40.120] dur=6.34s

**EN:** And you can tell it which format you want. So you might want JSON or you might want streaming JSON if you want to process this somehow.
**gemma:** И вы можете указать, в каком формате вам это нужно. Например, JSON или потоковый JSON, если вы хотите это как-то обработать.
**aya:** И вы можете указать, в каком формате хотите получить результат: JSON или потоковый JSON, если планируете его обрабатывать.

## [21:40.900 → 21:44.300] dur=3.40s

**EN:** So this is awesome for building on. We use this in CI all the time.
**gemma:** Это отлично для дальнейшего использования. Мы постоянно используем это в CI.
**aya:** Это отлично подходит для разработки. Мы постоянно используем это в CI (непрерывной интеграции).

## [21:44.800 → 21:47.780] dur=2.98s

**EN:** We use this for incident response. We use this in all sorts of pipelines.
**gemma:** Мы используем это для реагирования на инциденты. Мы используем это во всех видах пайплайнов.
**aya:** Мы используем это для реагирования на инциденты и во всех видах конвейеров.

## [21:48.400 → 21:52.400] dur=4.00s

**EN:** So really convenient. Just think of it as like a Unix utility. You give it a prompt. It gives you JSON.
**gemma:** Так очень удобно. Просто представьте это как утилиту Unix. Вы даёте ей запрос, а она выдаёт JSON.
**aya:** Очень удобно. Можно представить его как утилиту Unix: вы вводите запрос, а она возвращает JSON.

## [21:52.780 → 21:55.560] dur=2.78s

**EN:** You can use this in any way. You can pipe into it. You can pipe out of it.
**gemma:** Вы можете использовать это как угодно. Вы можете подавать данные в него и получать из него.
**aya:** Его можно использовать по-разному. Его можно прокачивать (pipe) внутрь и наружу.

## [22:00.010 → 22:07.490] dur=7.48s

**EN:** The piping is also pretty cool. So you can use, like, for example, get status and pipe this in and, you know, use JQ to select the result.
**gemma:** Пайпинг тоже довольно крут. Например, вы можете получить статус и подать это сюда, а затем использовать JQ, чтобы выбрать результат.
**aya:** Пропускание данных (piping) действительно круто. Можно использовать, например, для получения статуса и передачи его через `jq` для выбора нужного результата.

## [22:08.290 → 22:13.110] dur=4.82s

**EN:** The combinations are endless. And it's sort of this new idea. It's like a super intelligent Unix utility.
**gemma:** Комбинаций бесконечно много. И это новая идея. Это как суперумная утилита Unix.
**aya:** Возможности комбинаций безграничны. Это как новая идея — суперинтеллектуальная утилита Unix.

## [22:13.490 → 22:17.310] dur=3.82s

**EN:** And I think we barely scratched the surface of how to use this. We're just figuring this out.
**gemma:** И я думаю, мы едва начали разбираться, как это использовать. Мы только выясняем это.
**aya:** Я считаю, мы лишь начали осваивать возможности использования этого инструмента. Мы только начинаем его понимать.

## [22:18.570 → 22:25.330] dur=6.76s

**EN:** You can read from, like, a GCP bucket. Read, you know, like a giant log and pipe it in and tell Claude to figure out what's interesting about this log.
**gemma:** Вы можете читать из бакета GCP. Прочитать, знаете, огромный лог и подать его сюда, а затем попросить Claude выяснить, что интересного в этом логе.
**aya:** Можно читать данные из, например, бакета GCP. Читать, как гигантский лог, и передавать его через трубу (pipe), чтобы Claude анализировал и определял интересные моменты в логе.

## [22:26.090 → 22:32.130] dur=6.04s

**EN:** You can fetch data from, like, the Sentry CLI. You can also pipe it in and have Claude do something with it.
**gemma:** Вы можете получить данные из Sentry CLI. Вы также можете подать их сюда, и Claude что-то с ними сделает.
**aya:** Можно извлекать данные из, например, Sentry CLI. Также можно передавать эти данные через трубу и давать Claude выполнять с ними определённые действия.

## [22:38.040 → 22:42.580] dur=4.54s

**EN:** The final thing, and this is probably, like, the most advanced use cases we see. I'm sort of a Claude normie.
**gemma:** И последнее, и это, наверное, самый продвинутый сценарий использования. Я вроде как фанат Claude.
**aya:** Последнее — это, вероятно, самые сложные случаи использования. Я, так сказать, новичок в мире Claude.

## [22:43.040 → 22:51.980] dur=8.94s

**EN:** So I'll have usually, like, one Claude running at a time. And maybe I'll have, like, a few terminal tabs for a few different repos running at a time. When I look at power users in and out of Anthropic,
**gemma:** Обычно у меня запущено одно окно Claude. И, возможно, несколько вкладок терминала для разных репозиториев. Когда я смотрю на продвинутых пользователей в Anthropic,
**aya:** Обычно я запускаю одного Claude одновременно. У меня может быть несколько вкладок терминала для работы с разными репозиториями. Когда я наблюдаю за опытными пользователями внутри и вне Anthropic,

## [22:52.940 → 22:58.660] dur=5.72s

**EN:** almost always they're going to have, like, SSH sessions. They'll have, like, Tmux tunnels into their Claude sessions.
**gemma:** Почти всегда у них будут сессии SSH. Они будут использовать туннели Tmux в свои сессии Claude.
**aya:** Почти всегда у опытных пользователей есть сеансы SSH. Они используют туннели Tmux для подключения к своим сессиям Claude.

## [22:59.100 → 23:07.660] dur=8.56s

**EN:** They're going to have a bunch of checkouts of the same repo so that they can run a bunch of Claude in parallel in that repo. Or they're using Git work trees to have some kind of isolation as they do this.
**gemma:** У них будет много клонов одного и того же репозитория, чтобы запустить несколько Claude параллельно в нём. Или они используют Git work trees для некоторой изоляции при выполнении этого.
**aya:** Они создают несколько проверок одного и того же репозитория, чтобы запускать несколько Claude параллельно в этом репозитории. Или используют Git work trees для изоляции при выполнении этой задачи.

## [23:08.300 → 23:16.300] dur=8.00s

**EN:** And we're actively working on making this easier to use, but for now, like, these are some ideas for how to do more work in parallel with Claude.
**gemma:** И мы активно работаем над тем, чтобы это было проще использовать, но пока это лишь идеи о том, как выполнять больше работы с Claude параллельно.
**aya:** Мы активно работаем над упрощением этого процесса, но на данный момент вот несколько идей для выполнения больше работы параллельно с Claude.

## [23:16.660 → 23:18.220] dur=1.56s

**EN:** You can run as many sessions as you want.
**gemma:** Вы можете запустить столько сессий, сколько захотите.
**aya:** Вы можете запускать столько сессий, сколько хотите.

## [23:19.780 → 23:21.460] dur=1.68s

**EN:** And there's a lot that you can get done in parallel.
**gemma:** И вы можете выполнить много работы параллельно.
**aya:** И многое можно сделать параллельно.

## [23:24.680 → 23:28.100] dur=3.42s

**EN:** So, yeah, that's it. I wanted to also leave some time for Q&A.
**gemma:** Итак, вот и всё. Я также хотел оставить время для вопросов и ответов.
**aya:** Так что, да, это и есть всё. Я также хотел оставить время для вопросов и ответов.

## [23:28.680 → 23:31.020] dur=2.34s

**EN:** So I think this is the last slide that I have.
**gemma:** Думаю, это последний слайд.
**aya:** Думаю, это последняя слайд, который у меня есть.

## [23:31.600 → 23:34.180] dur=2.58s

**EN:** And, yeah, if folks have questions, there's mics on both sides.
**gemma:** Если у кого-то есть вопросы, микрофоны включены с обеих сторон.
**aya:** И если у кого-то возникнут вопросы, микрофоны находятся по обе стороны.

## [23:35.300 → 23:37.280] dur=1.98s

**EN:** And, yeah, we'd love to answer any questions.
**gemma:** Мы с удовольствием ответим на любые вопросы.
**aya:** И мы с удовольствием ответим на любые вопросы.

## [23:53.650 → 24:01.110] dur=7.46s

**EN:** I did. Hey, Boris.
**gemma:** Я сделал. Эй, Борис.
**aya:** Я тоже. Эй, Борис.

## [24:01.570 → 24:05.110] dur=3.54s

**EN:** Thanks for building a Cloud Code. And I was wondering what was the hardest
**gemma:** Спасибо за создание Cloud Code. Мне было интересно, что было самым сложным.
**aya:** Спасибо за создание Cloud Code. И я хотел бы узнать, что было самым сложным.

## [24:05.570 → 24:13.650] dur=8.08s

**EN:** implementation, like, part of the implementation for you of building it? I think there's a lot of tricky parts.
**gemma:** Внедрение, например, какая часть реализации для вас была самой сложной? Я думаю, там много хитростей.
**aya:** Самая сложная часть — это реализация, безусловно. В процессе создания такого решения приходится сталкиваться с множеством трикиных моментов.

## [24:14.750 → 24:20.390] dur=5.64s

**EN:** I think one part that is especially tricky is the things that we do to make bash commands safe.
**gemma:** Я думаю, особенно сложным является то, что мы делаем, чтобы сделать команды bash безопасными.
**aya:** Согласен, обеспечение безопасности команд Bash — действительно сложная задача.

## [24:21.430 → 24:25.570] dur=4.14s

**EN:** Bash is inherently pretty dangerous and it can change system state in unexpected ways.
**gemma:** Bash по своей природе довольно опасен и может неожиданно изменять состояние системы.
**aya:** Bash по своей природе опасен, так как может изменять состояние системы непредсказуемым образом.

## [24:26.270 → 24:36.210] dur=9.94s

**EN:** But at the same time, if you have to manually approve every single bash command, it's super annoying as an engineer. And you can't really be productive because you're just constantly approving every command.
**gemma:** Но в то же время, если нужно вручную одобрять каждую команду bash, это очень раздражает инженера. И ты не можешь быть продуктивным, потому что постоянно одобряешь каждую команду.
**aya:** Но если каждый командный запрос требует ручного одобрения, это действительно раздражает инженеров и снижает продуктивность.

## [24:36.950 → 24:47.330] dur=10.38s

**EN:** And just kind of navigating how to do this safely in a way that that scales across the different kinds of code bases people have because not everyone runs their code in a Docker container was pretty tricky.
**gemma:** И просто разобраться, как делать это безопасно и масштабируемо для разных кодовых баз, потому что не все запускают свой код в контейнере Docker, было довольно сложно.
**aya:** И поиск безопасного способа масштабирования этих мер для различных типов кодовых баз оказался сложной задачей, особенно учитывая, что не все используют Docker-контейнеры.

## [24:47.650 → 24:55.610] dur=7.96s

**EN:** And essentially the thing we landed on is there's some commands that are read-only. There's some static analysis that we do in order to figure out which commands can be combined in safe ways.
**gemma:** По сути, мы пришли к выводу, что некоторые команды являются только для чтения. Мы проводим статический анализ, чтобы определить, какие команды можно безопасно объединить.
**aya:** В итоге мы пришли к тому, что некоторые команды только для чтения, и проводим статический анализ для определения команд, которые можно безопасно комбинировать.

## [24:55.990 → 25:01.790] dur=5.80s

**EN:** And then we have this pretty complex tiered permission system so that you can allow list and block list commands at different levels.
**gemma:** И у нас есть довольно сложная многоуровневая система разрешений, которая позволяет разрешать и блокировать команды на разных уровнях.
**aya:** И у нас есть сложная многоуровневая система разрешений, позволяющая добавлять и блокировать команды на разных уровнях.

## [25:05.020 → 25:10.980] dur=5.96s

**EN:** Hi, Boris. You mentioned giving an image to Cloud Code, which made me wonder if there's some sort of
**gemma:** Привет, Борис. Ты упомянул передачу образа в Cloud Code, что заставило меня задуматься о том, есть ли какой-то
**aya:** Привет, Борис. Ты упоминал о предоставлении образа Cloud Code, что заставило меня задуматься: существует ли какой-то способ...

## [25:11.900 → 25:16.720] dur=4.82s

**EN:** multimodal functionality that I'm not aware of. Is that, are you just pointing it at an image on the file system or something?
**gemma:** мультимодальная функциональность, о которой я не знаю. Или ты просто указываешь на образ в файловой системе?
**aya:** Функциональность, о которой ты спрашиваешь, подразумевает работу с изображениями в Cloud Code. Это не просто указание на изображение в файловой системе, а использование передовых методов обработки и анализа изображений.

## [25:17.260 → 25:19.140] dur=1.88s

**EN:** Yeah, so Cloud Code is fully multimodal.
**gemma:** Да, Cloud Code полностью мультимодальный.
**aya:** Да, Cloud Code полностью многомодален.

## [25:19.480 → 25:23.240] dur=3.76s

**EN:** It has been from the start. It's in a terminal, so it's a little hard to discover.
**gemma:** Он был с самого начала. Он в терминале, так что его немного сложно обнаружить.
**aya:** Он с самого начала был многомодальным. Поскольку он работает в терминале, это может сделать его обнаружение немного сложнее.

## [25:24.120 → 25:32.760] dur=8.64s

**EN:** But yeah, you can take an image and just drag and drop it in. That'll work. You can give it a file path. That'll work. You can copy and paste the image in and that works too.
**gemma:** Но да, вы можете взять изображение и просто перетащить его. Это сработает. Вы можете указать путь к файлу. Это сработает. Вы можете скопировать и вставить изображение, и это тоже работает.
**aya:** Да, вы можете взять изображение и просто перетащить его в терминал. Также можно указать путь к файлу или вставить изображение с помощью копирования и вставки.

## [25:35.790 → 25:43.050] dur=7.26s

**EN:** This is pretty often for if I have like a mock of something, I'll just drag and drop in the mock. I'll tell it to implement it. I'll give it up a tier server so it can iterate against it.
**gemma:** Это довольно часто: если у меня есть макет чего-то, я просто перетаскиваю макет. Я прошу его реализовать это. Я даю ему тестовый сервер, чтобы он мог итерировать по нему.
**aya:** Часто так происходит, когда у меня есть макет чего-либо: я перетаскиваю макет в терминал, указываю ему реализовать его и предоставляю сервер для итераций.

## [25:43.450 → 25:44.950] dur=1.50s

**EN:** And yeah, it's just fully automated.
**gemma:** И да, это полностью автоматизировано.
**aya:** И да, это полностью автоматизировано.

## [25:48.670 → 25:52.710] dur=4.04s

**EN:** Hey, why did you build a CLI tool instead of an IDE?
**gemma:** Эй, почему ты создал CLI-инструмент, а не IDE?
**aya:** Привет! Я создал инструмент командной строки (CLI) вместо интегрированной среды разработки (IDE) по следующим причинам:

## [25:54.510 → 26:02.890] dur=8.38s

**EN:** Yeah, it's a good question. I think there's probably two reasons. One is we started this adanthropic. And in adanthropic, people use a broad range of IDEs.
**gemma:** Да, это хороший вопрос. Думаю, есть, наверное, две причины. Во-первых, мы начали adanthropic. И в adanthropic люди используют очень широкий спектр IDE.
**aya:** Да, это действительно хороший вопрос. Думаю, есть два основных причины:

## [26:03.250 → 26:08.790] dur=5.54s

**EN:** And some people use VS Code. Other people use Zed or Xcode or Vim or Emacs.
**gemma:** Кто-то использует VS Code. Другие — Zed, Xcode, Vim или Emacs.
**aya:** Некоторые используют Visual Studio Code, другие — Atom, Xcode, Vim или Emacs.

## [26:09.410 → 26:11.970] dur=2.56s

**EN:** And it was just hard to build something that works for everyone.
**gemma:** И было сложно создать что-то, что подойдет всем.
**aya:** И создать что-то, что подойдёт всем, было сложно.

## [26:12.370 → 26:14.230] dur=1.86s

**EN:** And so terminal is just the common denominator.
**gemma:** Поэтому терминал стал общим знаменателем.
**aya:** Терминал — это общий знаменатель.

## [26:15.010 → 26:17.110] dur=2.10s

**EN:** The second thing is adanthropic,
**gemma:** Второе — это античеловечность,
**aya:** Второе — антропоцентричное.

## [26:17.530 → 26:21.810] dur=4.28s

**EN:** we see up close how fast the model is getting better.
**gemma:** Мы видим вблизи, как быстро улучшается модель.
**aya:** Мы видим, как быстро модель совершенствуется.

## [26:22.210 → 26:26.110] dur=3.90s

**EN:** And so I think there's a good chance that by the end of the year, people aren't using IDEs anymore.
**gemma:** И поэтому я думаю, что к концу года люди перестанут использовать IDE.
**aya:** И я думаю, что к концу года у людей больше не будет использоваться ИДЭ (интегрированная среда разработки).

## [26:27.130 → 26:38.410] dur=11.28s

**EN:** And so we want to get ready for this future. And we want to avoid over-investing in UI and other layers on top, given that the way the models are progressing, it just may not be useful work pretty soon.
**gemma:** Поэтому мы хотим подготовиться к этому будущему. И мы хотим избежать чрезмерных инвестиций в пользовательский интерфейс и другие верхние слои, учитывая, что, судя по прогрессу моделей, эта работа скоро может оказаться бесполезной.
**aya:** И поэтому мы хотим подготовиться к этому будущему и избежать чрезмерных инвестиций в интерфейс пользователя и другие слои поверх, учитывая, что прогресс моделей может сделать эту работу ненужной довольно скоро.

## [26:42.380 → 26:46.120] dur=3.74s

**EN:** Yeah. How much have you... I don't know if this is... Is this on?
**gemma:** Да. Сколько вы... Я не знаю, включено ли это...
**aya:** Да. Насколько я... Я не уверен, правильно ли это называется, но, по-видимому, это работает.

## [26:46.820 → 26:55.240] dur=8.42s

**EN:** How much have you used plot code for machine learning modeling and almost that AutoML experience? I was curious what the experience has been so far with that.
**gemma:** Как много вы использовали Plot Code для моделирования машинного обучения и опыта AutoML? Мне было интересно, каков ваш опыт на данный момент.
**aya:** В какой степени вы использовали код для построения графиков при моделировании машинного обучения и каковой был ваш опыт с автоматизированным машинным обучением (AutoML)? Я заинтересован в том, каковы были ваши впечатления от этого процесса.

## [26:55.660 → 27:01.120] dur=5.46s

**EN:** Yeah. I think the question was, how much are we using quad code for machine learning and modeling?
**gemma:** Да. Я думаю, вопрос был о том, как много мы используем Plot Code для машинного обучения и моделирования.
**aya:** Да, кажется, вопрос заключался в том, насколько широко мы используем код для построения графиков при моделировании машинного обучения.

## [27:01.480 → 27:07.320] dur=5.84s

**EN:** We actually use it for this a bunch. So both engineers and researchers adanthropic use quad code every day.
**gemma:** На самом деле мы используем его очень часто. И инженеры, и исследователи Anthropic используют Plot Code каждый день.
**aya:** На самом деле, мы активно используем его для этого. И инженеры, и исследователи ежедневно применяют код для построения графиков в своей работе.

## [27:07.960 → 27:12.740] dur=4.78s

**EN:** I think about 80% of people adanthropic that are technical use quad code every day.
**gemma:** Я думаю, что около 80% технических сотрудников Anthropic используют Plot Code каждый день.
**aya:** По моим наблюдениям, около 80% технических специалистов в нашей организации используют код для построения графиков в повседневной работе.

## [27:13.320 → 27:17.300] dur=3.98s

**EN:** And hopefully you can see that in the product and kind of the amount of love and dog fooding we've put into it.
**gemma:** И, надеюсь, вы можете увидеть это в продукте и в объеме любви и доработки, которые мы в него вложили.
**aya:** И, надеюсь, вы видите результаты в продукте — в количестве усилий и внимания, которые мы вложили в его разработку.

## [27:17.960 → 27:23.020] dur=5.06s

**EN:** But this includes researchers who use tools like the notebook tool to edit and run notebooks.
**gemma:** Но это включает исследователей, которые используют такие инструменты, как блокнот, для редактирования и запуска блокнотов.
**aya:** Но это включает исследователей, которые используют инструменты, такие как ноутбук для редактирования и выполнения ноутбуков.

## [27:23.420 → 27:24.820] dur=1.40s

**EN:** Okay. Very cool. Thank you.
**gemma:** Хорошо. Очень круто. Спасибо.
**aya:** Спасибо. Приятно было помочь.

## [27:27.250 → 27:29.150] dur=1.90s

**EN:** All right. I think that's it. Thanks.
**gemma:** Хорошо. Думаю, на этом всё. Спасибо.
**aya:** Хорошо, думаю, это всё. Спасибо.
