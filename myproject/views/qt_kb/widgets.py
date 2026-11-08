"""Qt 知识：控件与布局"""

import streamlit as st


def render() -> None:
    st.write(
        "QWidget 是大多数界面元素的基类。QPushButton、QLineEdit、QLabel 是常用控件。"
        "不要用绝对坐标硬摆位置，优先用 QVBoxLayout、QHBoxLayout 这类布局，窗口缩放时控件会跟着调整。"
    )
