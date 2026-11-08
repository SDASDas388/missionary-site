"""Qt 知识：信号与槽"""

import streamlit as st


def render() -> None:
    st.write(
        "控件在发生事件时发出信号，例如按钮被点击。槽是用来响应该信号的函数。"
        "用 connect 把信号和槽接上之后，点击按钮就会调用对应函数，界面代码和业务代码因此分开。"
    )
