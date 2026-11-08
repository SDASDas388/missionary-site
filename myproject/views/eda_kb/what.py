"""EDA 知识：是什么"""

import streamlit as st


def render() -> None:
    st.write(
        "EDA 在这里指电子设计自动化（Electronic Design Automation）。"
        "它用软件完成电路原理图、仿真、印制电路板（PCB）布局布线，"
        "让硬件设计可以在计算机上检查，再送到工厂制板。"
    )
