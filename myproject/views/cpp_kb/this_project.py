"""C++ 知识：和本项目的关系"""

import streamlit as st


def render() -> None:
    st.write(
        "本站本身用 Python 编写，C++ 是旁边的一条学习线。"
        "理解编译、类型和对象生命周期之后，再看 Qt 的控件和信号槽会轻松很多："
        "Qt 的窗口、按钮本质上都是 C++ 对象。"
    )
