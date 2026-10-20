from pathlib import Path

import streamlit as st

RESOURCE_DIR = Path(__file__).resolve().parent.parent / "resource"
PROJECT_ICON = RESOURCE_DIR / "logo.ico"
PROJECT_SETUP = RESOURCE_DIR / "mysetup.exe"


def _read_setup() -> bytes:
    return PROJECT_SETUP.read_bytes()


def render():
    st.title("个人介绍")
    st.write(
        "我性格踏实稳重、积极好学，具备较强的自主学习能力和问题排查能力。"
        "平时做事认真细致，逻辑性强，遇到问题能够独立思考、耐心排查并总结经验。"
        "在技术方面，我熟悉 Python 基础开发、接口调用以及常见的程序调试方法，"
        "能够独立完成简单项目的开发与部署。"
    )
    st.write(
        "工作学习中我注重效率与细节，善于复盘优化，具备良好的执行力与团队协作意识。"
        "未来我希望继续深耕技术，不断提升自己的专业能力，持续学习、稳步进步。"
    )

    st.header("正在学习的方向")
    st.write("这个网站把目前在学的几块内容放在一起，方便自己复习，也方便别人快速了解。")
    st.markdown(
        """
- **Python**：写脚本、调接口、用 Streamlit 做这个网站
- **C++**：理解编译、内存和面向对象，为更底层的开发打底
- **Qt**：用 C++ 做桌面界面，掌握信号与槽、布局和事件循环
- **EDA**：了解从原理图、仿真到 PCB 的电子设计流程
        """
    )

    st.header("个人项目")
    # 下载按钮盖在图标上，点击图片即可下载安装包。安装包约 49MB，点下去才读取。
    st.html(
        """
        <style>
        .st-key-project_download {
            position: relative;
            width: fit-content;
        }
        .st-key-project_download .st-key-download_mysetup {
            position: absolute !important;
            top: 0;
            left: 0;
            width: 160px;
            height: 160px;
            margin: 0 !important;
            z-index: 3;
        }
        .st-key-project_download .st-key-download_mysetup button {
            width: 160px;
            height: 160px;
            min-height: 160px;
            opacity: 0;
            cursor: pointer;
        }
        </style>
        """
    )
    with st.container(key="project_download", width="content"):
        st.image(PROJECT_ICON, width=160, alt="个人项目图标")
        st.download_button(
            "下载我的项目",
            data=_read_setup,
            file_name="mysetup.exe",
            mime="application/octet-stream",
            key="download_mysetup",
            on_click="ignore",
        )
