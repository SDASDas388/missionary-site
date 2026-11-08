"""Python 知识：运行与环境"""

import streamlit as st


def render() -> None:
    st.write(
        "脚本可以直接用 python 文件名.py 运行。网页应用则用 streamlit run 启动，"
        "浏览器里每次操作都会让脚本从头再执行一遍。虚拟环境用来固定依赖版本，避免和系统里别的项目打架。"
    )
