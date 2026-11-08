"""EDA 知识：PCB 与常见工具"""

import streamlit as st


def render() -> None:
    st.write(
        "PCB 设计把原理图变成铜箔走线、过孔和器件摆放，同时要考虑线宽、间距、地层和干扰。"
        "入门常用 KiCad，工业场景里常见 Altium Designer。两者都覆盖原理图捕获和 PCB 布局。"
    )
