"""Python 知识：和本项目的关系"""

import streamlit as st


def render() -> None:
    st.write(
        "首页的 AI 助手就是一个 Python 程序：Streamlit 负责页面和输入框，"
        "openai 库负责把问题发给模型，json 模块负责把每一段会话写进 sessions 目录。"
        "另外五个页面也是 Python 函数，由启动文件按按钮调用。"
    )
