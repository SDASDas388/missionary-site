import runpy
from pathlib import Path

import streamlit as st

from views.cpp_kb import render as render_cpp
from views.eda_kb import render as render_eda
from views.intro import render as render_intro
from views.python_kb import render as render_python
from views.qt_kb import render as render_qt

ROOT = Path(__file__).resolve().parent
PAGE_NAMES = ["AI 助手", "个人介绍", "Python 知识", "C++ 知识", "Qt 知识", "EDA 知识"]

st.set_page_config(
    page_title="missionary星球",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "# 这将是missionary的个人网站"
    },
)

# 首页脚本自己也会调用 set_page_config。站点配置以本文件为准，
# 所以这里把它换成空操作，再去执行原来的 ai_partner.py。
st.set_page_config = lambda *args, **kwargs: None


def select_page(name: str) -> None:
    st.session_state.current_page = name
    st.rerun()


if "current_page" not in st.session_state:
    st.session_state.current_page = "AI 助手"

with st.container(horizontal=True, horizontal_alignment="center", gap="small"):
    for name in PAGE_NAMES:
        st.button(
            name,
            key=f"nav_{name}",
            width="content",
            type="primary" if st.session_state.current_page == name else "secondary",
            on_click=select_page,
            args=(name,),
        )

current_page = st.session_state.current_page
if current_page == "AI 助手":
    runpy.run_path(str(ROOT / "ai_partner.py"), run_name="ai_partner_page")
elif current_page == "个人介绍":
    render_intro()
elif current_page == "Python 知识":
    render_python()
elif current_page == "C++ 知识":
    render_cpp()
elif current_page == "Qt 知识":
    render_qt()
elif current_page == "EDA 知识":
    render_eda()
