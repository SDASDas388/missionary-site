import streamlit as st


def render():
    st.title("Python 知识")

    st.header("是什么")
    st.write(
        "Python 是一门解释型、强调可读性的通用语言。"
        "同一份代码可以写自动化脚本、调用网络接口，也可以像本站这样做成交互页面。"
        "它不需要单独的编译步骤，改完保存后重新运行就能看到结果。"
    )

    st.header("核心概念")
    st.subheader("数据与函数")
    st.write(
        "常用类型有字符串、列表、字典和布尔值。函数用 def 定义，把一段重复逻辑收起来，"
        "调用时传入参数、拿回返回值。字典很适合保存「名字到内容」这种结构，"
        "本站的聊天记录就是用字典列表来存的。"
    )
    st.subheader("模块与导入")
    st.write(
        "一个 .py 文件就是一个模块。用 import 把别的模块引进来，避免所有代码堆在一个文件里。"
        "标准库提供 json、os、datetime 这类工具；第三方库用 pip 安装，例如 streamlit 和 openai。"
    )
    st.subheader("运行与环境")
    st.write(
        "脚本可以直接用 python 文件名.py 运行。网页应用则用 streamlit run 启动，"
        "浏览器里每次操作都会让脚本从头再执行一遍。虚拟环境用来固定依赖版本，避免和系统里别的项目打架。"
    )

    st.header("和本项目的关系")
    st.write(
        "首页的 AI 助手就是一个 Python 程序：Streamlit 负责页面和输入框，"
        "openai 库负责把问题发给模型，json 模块负责把每一段会话写进 sessions 目录。"
        "另外五个页面也是 Python 函数，由启动文件按按钮调用。"
    )
