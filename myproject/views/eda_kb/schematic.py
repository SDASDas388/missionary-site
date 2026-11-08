"""EDA 知识：原理图"""

import streamlit as st


def render() -> None:
    st.write(
        "原理图用符号表示电阻、电容、芯片和连接关系，讲的是「谁和谁相连」，还不是物理位置。"
        "每个元件要有封装，封装描述它在板上的焊盘形状，后面才能落到 PCB。"
    )
