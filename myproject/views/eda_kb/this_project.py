"""EDA 知识：和本项目的关系"""

import streamlit as st


def render() -> None:
    st.write(
        "Python、C++ 和 Qt 解决的是软件与界面，EDA 解决的是这些程序要对话的电路。"
        "把四块放在同一个网站里，是为了把「写程序」和「看电路」连成一条学习线："
        "接口、界面和板级信号可以对照着记。"
    )
