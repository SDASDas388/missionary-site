"""Qt 知识：是什么"""

import streamlit as st


def render() -> None:
    st.write(
        "Qt 是一套用 C++ 编写的跨平台应用框架，最常见的用途是做桌面图形界面。"
        "它提供窗口、按钮、输入框、布局管理器，以及自己的事件循环。"
        "同一套界面代码可以在 Windows、Linux 和 macOS 上编译运行。"
    )
