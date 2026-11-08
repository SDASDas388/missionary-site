"""Python 知识：模块与导入"""

import streamlit as st


def render() -> None:
    st.write(
        "一个 .py 文件就是一个模块。用 import 把别的模块引进来，避免所有代码堆在一个文件里。"
        "标准库提供 json、os、datetime 这类工具；第三方库用 pip 安装，例如 streamlit 和 openai。"
    )
