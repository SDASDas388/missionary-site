from pathlib import Path

import streamlit as st

from views.chapters import select_chapter

RESOURCE_DIR = Path(__file__).resolve().parent.parent / "resource"
PROJECT_ICON = RESOURCE_DIR / "logo.ico"
PROJECT_SETUP = RESOURCE_DIR / "mysetup.exe"

CHAPTERS = [
    "自我介绍",
    "正在学习的方向",
    "个人项目",
]


def _read_setup() -> bytes:
    return PROJECT_SETUP.read_bytes()


def _about() -> None:
    st.write(
        "我性格踏实稳重、积极好学，具备较强的自主学习能力和问题排查能力。"
        "平时做事认真细致，逻辑性强，遇到问题能够独立思考、耐心排查并总结经验。"
        "在技术方面，我熟悉 Python 基础开发、接口调用以及常见的程序调试方法，"
        "能够独立完成简单项目的开发与部署。"
    )
    st.write(
        "工作学习中我注重效率与细节，善于复盘优化，具备良好的执行力与团队协作意识。"
        "未来我希望继续深耕技术，不断提升自己的专业能力，持续学习、稳步进步。"
    )


def _learning() -> None:
    st.write("这个网站把目前在学的几块内容放在一起，方便自己复习，也方便别人快速了解。")
    st.markdown(
        """
- **Python**：写脚本、调接口、用 Streamlit 做这个网站
- **C++**：理解编译、内存和面向对象，为更底层的开发打底
- **Qt**：用 C++ 做桌面界面，掌握信号与槽、布局和事件循环
- **EDA**：了解从原理图、仿真到 PCB 的电子设计流程
        """
    )


def _project_download() -> None:
    # 下载按钮盖在图标上，点击图片即可下载安装包。安装包约 49MB，点下去才读取。
    st.html(
        """
        <style>
        .st-key-project_download {
            position: relative;
            width: fit-content;
        }
        .st-key-project_download .st-key-download_mysetup {
            position: absolute !important;
            top: 0;
            left: 0;
            width: 160px;
            height: 160px;
            margin: 0 !important;
            z-index: 3;
        }
        .st-key-project_download .st-key-download_mysetup button {
            width: 160px;
            height: 160px;
            min-height: 160px;
            opacity: 0;
            cursor: pointer;
        }
        </style>
        """
    )
    with st.container(key="project_download", width="content"):
        st.image(PROJECT_ICON, width=160, alt="王室斗地主图标")
        st.download_button(
            "下载王室斗地主",
            data=_read_setup,
            file_name="mysetup.exe",
            mime="application/octet-stream",
            key="download_mysetup",
            on_click="ignore",
        )
    st.markdown(
        """点击图标可下载软件"""
    )


def _project_overview() -> None:
    st.markdown(
        """
王室斗地主是一款单机桌面游戏：一名真人玩家对两名 AI。
技术栈是 **C++17**、**Qt 6.11**（Widgets / Multimedia）、**CMake**、MinGW 64 位、Qt 资源系统和 JSON 配置。
代码约 **25 个类、5000 行**，图片 91 张，音频 163 段。

开发按层推进，先写不依赖窗口的数据和规则，再写游戏控制，最后接主界面、动画和音效，并打成绿色版和安装包。每一层都能单独核对行为。
        """
    )
    st.markdown(
        """
| 阶段 | 内容 |
|---|---|
| 模块 | Card、Cards、CardPanel、Player、Robot、UserPlayer、GameControl |
| 主界面 | 按钮组、分数与结算面板，以及叫分、出牌线程和 PlayHand、Strategy |
| 动画音效 | 背景音乐、加载页、特效窗口、倒计时 |
| 发布 | `windeployqt` 绿色版，以及带程序图标的安装包 |
        """
    )
    st.markdown(
        """
| 模块 | 做什么 |
|---|---|
| 启动 | 无边框透明加载窗，进度条走完进入主界面 |
| 发牌 | 54 张牌洗牌，定时器驱动发牌动画；每人 17 张，留 3 张底牌 |
| 叫地主 | 不叫 / 1 / 2 / 3 分，每人一次；叫 3 分直接当地主，三人都不叫就重发 |
| 出牌 | 识别并比较 20 种牌型；支持单击、拖动多选和右键出牌 |
| AI | 按手牌权重叫分；出牌时区分队友和对手，并考虑拆牌、留大牌、封堵报单 |
| 计时 | 需要压牌时倒计时 15 秒，最后 5 秒提示，超时自动不出 |
| 特效与音效 | 顺子、连对、飞机、炸弹、王炸的帧动画；背景音乐循环，男女声播报牌型 |
| 计分 | 底分取叫分，每出一个炸弹翻倍；地主按 2 倍结算，农民各按 1 倍 |
        """
    )


def _project_architecture() -> None:
    st.markdown(
        """
项目按 **数据层 → 逻辑层 → 界面层** 分开。上层直接调用下层的方法，下层只通过 Qt 信号往上通知，不反向依赖窗口。
        """
    )
    st.mermaid_chart(
        """
flowchart TB
    GP[GamePanel] -->|调用| GC[GameControl]
    GC -.->|信号| GP
    GC -->|虚函数| PL[Player]
    PL -.->|信号| GC
    PL --> RB[Robot]
    PL --> UP[UserPlayer]
    RB --> TH[AI 线程]
    TH --> ST[Strategy]
    ST --> PH[PlayHand]
    PH --> CD[Cards]
        """,
        alt="王室斗地主调用链：界面调用控制器，控制器通过玩家虚函数进入 AI",
    )
    st.markdown(
        """
界面上的按钮、牌面、动画和音效都挂在 GamePanel 这一侧，图里不再逐个展开。分层时守住这三条：

- **调用往下，通知往上。** GamePanel 持有 GameControl，例如直接调用 `startLordCard()`。GameControl 不知道界面的存在，只发出 `playerStatusChanged`、`gameStatusChanged`、`notifyPlayHand` 这类信号。规则可以单独验证，以后换成 QML 也不用改逻辑层。
- **面向 Player 抽象。** GameControl 只保存 `Player*`。轮到谁就调用 `preparePlayHand()`，运行时落到 Robot（启动 AI 线程）或 UserPlayer（启动倒计时，等玩家点按钮）。
- **数据层不引用任何 Widget。** Card、Cards、PlayHand、Strategy 只用 C++ 和 Qt 容器。

| 模式 | 在项目里的位置 |
|---|---|
| 观察者 | 层与层、玩家与控制器之间的通信都走信号槽 |
| 状态机 | `GameStatus` 管发牌 / 叫地主 / 出牌，`PlayerStatus` 管思考叫分、思考出牌和获胜 |
| 多态 / 模板方法 | Player 规定 `prepare*` 与 `think*` 四个虚函数，机器人和真人各自实现 |
| 中介者 | 三个玩家互不调用，出牌信息由 GameControl 用 `pendingInfo` 广播 |
| 对象池 | 启动时创建 54 个 CardPanel，放进 `QMap<Card, CardPanel*>`，对局中只改显示和位置 |
| 策略 | 出牌决策集中在 Strategy，和玩家对象分开 |
| 配置驱动 | 音频列表写在 `conf/playList.json`，枚举值就是下标，换文件不用改代码 |
        """
    )


def _project_classes() -> None:
    st.markdown("#### 数据层")
    st.markdown(
        """
| 类 | 职责 | 设计要点 |
|---|---|---|
| Card | 一张牌：点数 + 花色 | 点数枚举按大小排列，枚举值可以直接比大小；重载 `==`、`<` 并实现 `qHash`，能放进 `QSet`，也能当 `QMap` 的键 |
| Cards | 手牌、出的牌、底牌 | 底层是 `QSet<Card>`，不重复，查找是 O(1)，并集和差集对应拿牌和出牌；显示时再用 `toCardList` 排成有序向量 |
| Player | 玩家基类 | 保存手牌、角色、上下家，以及最近一次出牌。`grabLordBet` / `playHand` 只把操作包装成信号，自己不判规则 |
| Robot | 机器人 | `prepare*` 打开子线程，`think*` 在子线程里调用 Strategy |
| UserPlayer | 真人 | 叫分时什么都不做，等按钮；出牌时发出 `startCountDown` |
| PlayHand | 牌型识别和比较 | 用牌型、主体点数、附加长度三个字段描述一手牌 |
| Strategy | AI 出牌 | 主动出牌、找能压过的牌、决定出不出，以及最优顺子拆法 |
        """
    )
    st.markdown("#### 逻辑层与界面层")
    st.markdown(
        """
| 类 | 职责 |
|---|---|
| GameControl | 创建三名玩家并排好逆时针顺序，负责洗牌、叫分状态机、出牌、炸弹翻倍和结算，再把状态发给界面 |
| BetRecord | 记下当前最高叫分、是谁叫的、已经叫了几次 |
| Loading | 无边框透明启动页，定时器逐步截取进度条图片 |
| GamePanel | 主窗口：摆场景、响应 GameControl 的信号、排牌、处理选牌和特效 |
| CardPanel | 在 `paintEvent` 里画牌面或牌背，点击后发出 `cardSelected` |
| ButtonGroup | 用堆叠页面切换开始、出牌、不要、叫地主等按钮；叫分时藏掉不超过当前最高分的按钮 |
| AnimationWindow | 炸弹、王炸的帧动画，飞机平移，以及顺子、连对、叫分提示 |
| CountDown / ScorePanel / EndingPanel | 15 秒倒计时、分数条、从顶部弹入的结算面板 |
| BGMControl | 五个播放器，分别管男声、女声、背景音乐、辅助音效和结束音乐 |
        """
    )


def _project_flow() -> None:
    st.markdown("整局游戏由发牌、叫地主、出牌、结算四个状态推动。出牌阶段由三家轮流，直到有人出完。三人都不叫就回到发牌。")
    st.mermaid_chart(
        """
stateDiagram-v2
    [*] --> 发牌: 点击开始
    发牌 --> 叫地主: 底牌只剩三张
    叫地主 --> 发牌: 三人都不叫
    叫地主 --> 出牌: 产生地主
    出牌 --> 结算: 有人出完
    结算 --> 发牌: 继续游戏
        """,
        alt="斗地主对局状态机：发牌、叫地主、出牌、结算",
    )
    st.markdown(
        """
**发牌。** 动画用定时器每 10 毫秒走一步，左右两家沿水平方向、自己沿垂直方向移动，步长由起终点距离除以 100 得到。一张牌走到终点，才从牌堆里随机取出并交给当前玩家。玩家拿到牌后发出 `notifyPickCards`，界面再刷新。画面和手牌数据因此始终对齐。

**叫地主。** `GameControl::onGrabBet` 按这次叫分更新记录：没超过当前最高分视为不抢，第一个叫分的是叫地主，后面的是抢地主。叫 3 分立刻成为地主；三人都叫过之后，最高分为 0 就重发，否则最高分的人当地主。地主拿走三张底牌，一秒后进入出牌。

**出牌。** 真人出牌前做五层检查：当前是出牌阶段、轮到自己、选了牌、牌型合法、压得过上家。机器人在子线程里算出结果，同样走 `playHand`。炸弹和王炸让当前底分翻倍。手牌出完就按角色结算，否则轮到下家。

这里不用回合计数器。玩家选择不出时，不更新 `pendPlayer`。另外两家都过后，又轮到上次出牌的人，此时 `pendPlayer` 就是自己，表示拿到自由出牌权。界面只显示出牌按钮，AI 进入 `firstPlay()`，倒计时也不启动。

**计分。** 底分等于叫分，每出一个炸弹或王炸再乘 2。地主赢则地主加 2 倍底分、两名农民各扣 1 倍；农民赢则两名农民各加 1 倍、地主扣 2 倍。输赢由上下家指针和角色推出来。
        """
    )


def _project_algorithm() -> None:
    st.markdown(
        """
**牌型。** PlayHand 先按点数计数，再按出现次数分进单张、对子、三张、四张四个桶。每种牌型就是这四个桶的大小，再加上点数是否连续。一手牌最多 20 张，计数是 O(n)，判断是常数级。

比较时按这个顺序：牌型不合法不能出；对方是不出则任意合法牌都能出；王炸必胜；炸弹压普通牌型；牌型相同就比主体点数，顺子和连对还要求长度相同。`HandType` 里普通牌型连续定义，是否普通牌可以直接做区间判断。
        """
    )
    st.markdown(
        """
| 牌型 | 桶的条件 | 附加条件 |
|---|---|---|
| 单 / 对 / 三张 | 只有对应的一个桶 | — |
| 三带一 / 三带二 | 一组三张，再加一张或一对 | — |
| 飞机及带牌 | 两组相邻三张 | 点数小于 2 |
| 顺子 / 连对 | 至少五张单，或至少三组对 | 连续，且范围在 3 到 A |
| 炸弹 / 王炸及带牌 | 一组四张，或同时有大小王 | — |
        """
    )
    st.markdown(
        """
**叫分。** 机器人给手牌打权重：大小王每张 6 分，最优顺子和炸弹各 5 分，每张 2 记 3 分，去掉这些之后的三张每组 4 分，剩下的对子每组 1 分。已经计过的牌会从后续统计里拿掉，避免一张牌算两次。权重大于等于 22 叫 3 分，18 到 21 叫 2 分，10 到 17 叫 1 分，再低就不叫。

**出牌策略。** 自由出牌和压牌分开。自由出牌时优先处理难出的组合：能一次出完就出完；出顺子能减少单牌就出顺子；炸弹先留着；然后按连对、飞机、三张的顺序找；最后才出单牌和对子。下家是对手并且只剩一张时从大到小出，堵住报单，否则从小到大出。

压牌时，对手剩余不超过三张就直接考虑炸弹或王炸；先把最优顺子从手里拿开再找能压的牌，找不到才拆顺子。下家是对手且只剩一两张时用最大的能压的牌，否则用最小的。上家是队友时，不用 2 和大小王去压；上家是对手、双方牌都还多时，也不早早用对 2。
        """
    )
    st.mermaid_chart(
        """
flowchart TD
    A[makeStrategy] --> B{上次出牌的人是自己?}
    B -->|是| C["firstPlay：先出难处理的牌"]
    B -->|否| D[getGreaterCards 找出能压过的牌]
    D --> E{whetherToBeat 这手值得出吗}
    E -->|是| F[出牌]
    E -->|否| G[不出]
        """,
        alt="AI 出牌先判断自由出牌还是压牌，再决定出不出",
    )
    st.markdown(
        """
最优顺子用回溯枚举拆法：先拿走炸弹和三张，再递归尝试每一种顺子，最后给剩下的单牌打分。每张单牌的分数是点数加 15，多一张单牌的代价会盖过点数差异，所以先保证单牌最少，再让剩下的单牌尽量小。顺子和连对的搜索几乎一样，用成员函数指针换成“每个点数要几张、最短多长”，两套规则走同一段代码。
        """
    )


def _project_runtime() -> None:
    st.markdown(
        """
#### 多线程

机器人思考时会停两秒，让玩家看清过程。这段等待如果写在主线程，动画、倒计时和声音会一起卡住，所以思考放在 `QThread` 里。

`notifyGrabLordBet` 和 `notifyPlayHand` 在子线程发出，接收者 GameControl 在主线程。默认的 `AutoConnection` 发现线程不同，就改走排队连接：参数被复制进主线程事件队列，槽函数仍在主线程执行。界面刷新和游戏状态修改因此都留在主线程。`Cards` 要能被排队复制，所以在 `main` 里用 `qRegisterMetaType` 注册。线程对象在 `finished` 时 `deleteLater`，跑完自己释放。

#### 界面

54 张牌画在一张雪碧图上，启动时切成 54 张正面和 1 张背面。每张牌对应一个常驻的 CardPanel，之后发牌、出牌、重开都只做显示、隐藏和移动。

三个座位的差异收进 `PlayerContext`：手牌区域、出牌区域、横竖排列、正反面、提示文字、头像，以及这一轮打出的牌。`updatePlayerCards` 用同一套逻辑刷新所有玩家。

牌是叠放的，每张只露出约 20 像素，点击范围不能用控件的完整矩形。布局时把露出的区域记进哈希表，拖动时用鼠标位置判断划过哪张牌，并记住上一张，避免同一张牌被来回切换。选中的牌上移 10 像素，右键直接出牌。

| 动画 | 做法 |
|---|---|
| 发牌 | 定时器 10 毫秒一步 |
| 炸弹 / 王炸 | 定时器 60 毫秒换一帧，播完停止并隐藏 |
| 飞机 | 定时器 15 毫秒向左移 5 像素，同时轮换 5 帧 |
| 结算面板 | 属性动画配合 `OutBounce`，1.5 秒从顶部弹到中间 |
| 加载进度 | 定时器每次多截取一段进度条图片 |

#### 音效与 Qt 6

五个 `QMediaPlayer` 分开管语音、背景音乐、辅助音效和结束音乐，可以同时响、互不打断。播放列表在 JSON 里，`CardType` 的枚举值就是列表下标，跟牌时组合牌型会随机播“大你”。报单、报双如果和出牌语音撞上，就延迟 1.5 秒。

项目从 Qt 5 的写法迁到 Qt 6.11，多媒体模块变化最大：

| Qt 5 | Qt 6 里的处理 |
|---|---|
| `QMediaPlaylist` | 改用 `QVector<QVector<QUrl>>`，`setSource` 之后 `play` |
| `setVolume(0~100)` | 每个播放器配一个 `QAudioOutput`，音量改为 0.0 到 1.0 |
| 列表循环模式 | `setLoops(Infinite)` 或 `setLoops(1)` |
| `state()` | `playbackState()` |
| `qHash` 返回 `uint` | 改为 `size_t` |
| `QImage::mirrored()` | `image.flipped(Qt::Horizontal)` |
| qmake | CMake 与 `qt_add_executable` |
        """
    )


def _project_notes() -> None:
    st.markdown(
        """
实现过程里有几处直接决定了现在的写法：

- 信号槽会累加。开新局如果再次 `connect`，点一次按钮就会出多次牌。所有连接只在构造时做一次，新局只切换按钮页面。
- AI 的停顿必须离开主线程，否则窗口会卡住。计算结果再用信号送回主线程。
- 跨线程传递 `Cards` 时，类型没有注册就无法排队，槽函数不会被调用。注册元类型之后，参数才能复制到主线程。
- Qt 6 删除了 `QMediaPlaylist`，播放列表和循环要自己管。

后面还可以沿着同一套分层继续收：

- 子线程目前会读玩家手牌。思考期间主线程不会改这些数据，但更稳妥的做法是先复制手牌、上家的牌和各家剩余张数，子线程只做计算。AI 计算本身只要几毫秒，两秒停顿也可以改成主线程定时器；线程留到搜索变重的时候再用。
- 发牌进度和部分动画用了函数里的 `static` 变量，改成成员后，重置和多实例都更清楚。只读接口补上 `const` 之后，界面层也不必再去掉常量。
- PlayHand 和 Strategy 不依赖窗口，适合用 Qt Test 覆盖 20 种牌型和压牌规则。
- 加倍、明牌、春天、提示都可以加在现有状态机上，提示直接复用 `Strategy::getGreaterCards`。若要做成网络对战，GameControl、Player 和 PlayHand 可以放到服务端当权威状态，客户端保留 GamePanel，把本地信号换成网络消息。出牌是否合法在服务端再用 `PlayHand::canBeat` 校验一次，断线后的托管也可以直接用现在的 Strategy。
        """
    )


def _project() -> None:
    _project_download()
    st.subheader("王室斗地主")
    overview, architecture, classes, flow, algorithm, runtime, notes = st.tabs(
        ["概览", "分层", "类职责", "对局流程", "牌型与 AI", "界面与运行时", "实现取舍"]
    )
    with overview:
        _project_overview()
    with architecture:
        _project_architecture()
    with classes:
        _project_classes()
    with flow:
        _project_flow()
    with algorithm:
        _project_algorithm()
    with runtime:
        _project_runtime()
    with notes:
        _project_notes()


_BODY = {
    "自我介绍": _about,
    "正在学习的方向": _learning,
    "个人项目": _project,
}


def render() -> None:
    chapter = select_chapter("intro", CHAPTERS, page_title="个人介绍")
    st.title("个人介绍")
    st.header(chapter)
    _BODY[chapter]()
