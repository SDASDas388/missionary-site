# missionary星球

个人网站。顶部按钮切换页面：AI 助手负责对话，其余页面是个人介绍和分章节的知识笔记。

## 启动

在本目录（含 `app.py` 的目录）执行：

```powershell
pip install -r requirements.txt
streamlit run app.py
```

浏览器打开 http://localhost:8501 。改完代码保存后，页面会自动重新运行。

依赖只有两项：`streamlit==1.66.0`、`openai==3.35.1`。AI 对话走 DeepSeek 的 OpenAI 兼容接口。

密钥放在 `.streamlit/secrets.toml`，这个文件已被 `.gitignore` 排除，不要提交：

```toml
DEEPSEEK_API_KEY = "你的 DeepSeek API Key"
```

没有这个文件时，知识页和个人介绍仍能打开。进入「AI 助手」会因为读不到密钥而报错。

## 架构

整个站点是一个 Streamlit 脚本。`app.py` 是唯一入口，先画顶部导航，再按当前页面调用对应模块。浏览器里每一次点击都会让脚本从头执行一遍，跨次点击要保留的数据放在 `st.session_state` 里。

```text
浏览器
  │
  ▼
app.py                         页面配置、顶部六个按钮、按 current_page 分发
  ├─ ai_partner.py             AI 助手（用 runpy 按脚本执行）
  │    ├─ .streamlit/secrets.toml
  │    ├─ sessions/*.json      聊天记录
  │    └─ resource/logo.png
  └─ views/
       ├─ chapters.py          知识页共用的章节侧边栏
       ├─ knowledge.py         四门知识页共用的标题和分发
       ├─ intro.py             个人能力
       ├─ python_kb/           每一章一个文件
       ├─ cpp_kb/
       ├─ qt_kb/
       └─ eda_kb/
```

### 页面怎么切

`PAGE_NAMES` 决定顶部按钮的名字和顺序。点击按钮时，`select_page` 把名字写入 `st.session_state.current_page`，然后重新运行。默认页是「AI 助手」。

「AI 助手」不走 `render()`，而是用 `runpy.run_path` 执行 `ai_partner.py`。那个文件自己也会调用 `st.set_page_config`，所以 `app.py` 在导入之后把这个函数换成空操作，站点标题、图标和宽布局以 `app.py` 为准。

其余五个页面各自导出 `render()`，由 `app.py` 直接调用。

### 章节侧边栏

个人能力和四门知识页共用 `views/chapters.py` 的 `select_chapter`。它在左侧画出当前页的章节按钮，把选中的章节名记在 `chapter_memory_<页面键>` 里。这个键不属于按钮本身，所以切到别的顶部页面再回来，仍停在上次那一章。

四门知识页各自是一个包。章节正文在单独的文件里，包的 `__init__.py` 只按侧边栏顺序登记它们。例如 `views/cpp_kb/__init__.py`：

```python
_CHAPTERS = [
    ("前言", render_preface),
    ("类型与内存", render_memory),
]

def render() -> None:
    render_page("cpp", "C++ 知识", _CHAPTERS)
```

加一章时，在对应包里新建一个文件，写出 `render()`，再在 `_CHAPTERS` 末尾加一项。`render_page` 的页面键各页不要重复。

### AI 助手

`ai_partner.py` 在侧边栏放会话控制，主区域是聊天记录和输入框。

- 客户端：`OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")`
- 模型：`deepseek-flash`，流式输出
- 系统提示词用侧边栏里的「昵称」和「性格」填充
- 一次会话写成 `sessions/<时间戳>.json`，字段是 `nick_name`、`nature`、`current_session`、`messages`
- `sessions/*.json` 已在 `.gitignore` 里，换机器不会带上聊天记录

「新建会话」会先保存当前记录，再清空消息并换一个新的时间戳文件名。

## 目录

| 路径 | 作用 |
| --- | --- |
| `app.py` | 站点入口 |
| `ai_partner.py` | AI 助手页面 |
| `views/chapters.py` | 章节侧边栏 |
| `views/knowledge.py` | 知识页共用的标题和章节分发 |
| `views/intro.py` | 个人能力，含项目图标下载 |
| `views/python_kb/` | Python 知识，每章一个文件 |
| `views/cpp_kb/` | C++ 知识，每章一个文件 |
| `views/qt_kb/` | Qt 知识，每章一个文件 |
| `views/eda_kb/` | EDA 知识，每章一个文件 |
| `resource/` | 图标、安装包等静态文件 |
| `.streamlit/secrets.toml` | API 密钥，不入库 |
| `sessions/` | 聊天记录，不入库 |
| `requirements.txt` | Python 依赖 |
| `deepseekuse.py` | 早期的单次调用试验，不参与网站 |
| `streamlit.py` | 早期的页面试验，不参与网站 |

个人介绍里的下载按钮使用 `resource/logo.ico` 和 `resource/mysetup.exe`。安装包在点击下载时才读取。
