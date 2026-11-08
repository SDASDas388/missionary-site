"""Qt 知识：事件循环"""

import streamlit as st


def render() -> None:
    st.write(
        "QApplication 启动后进入 exec，程序停在事件循环里等待鼠标、键盘和定时器。"
        "界面相关操作应发生在这个循环所在的线程。耗时计算如果直接写在槽函数里，窗口会卡住。"
    )
