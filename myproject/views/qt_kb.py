import streamlit as st


def render():
    st.title("Qt 知识")

    st.header("是什么")
    st.write(
        "Qt 是一套用 C++ 编写的跨平台应用框架，最常见的用途是做桌面图形界面。"
        "它提供窗口、按钮、输入框、布局管理器，以及自己的事件循环。"
        "同一套界面代码可以在 Windows、Linux 和 macOS 上编译运行。"
    )

    st.header("核心概念")
    st.subheader("信号与槽")
    st.write(
        "控件在发生事件时发出信号，例如按钮被点击。槽是用来响应该信号的函数。"
        "用 connect 把信号和槽接上之后，点击按钮就会调用对应函数，界面代码和业务代码因此分开。"
    )
    st.subheader("控件与布局")
    st.write(
        "QWidget 是大多数界面元素的基类。QPushButton、QLineEdit、QLabel 是常用控件。"
        "不要用绝对坐标硬摆位置，优先用 QVBoxLayout、QHBoxLayout 这类布局，窗口缩放时控件会跟着调整。"
    )
    st.subheader("事件循环")
    st.write(
        "QApplication 启动后进入 exec，程序停在事件循环里等待鼠标、键盘和定时器。"
        "界面相关操作应发生在这个循环所在的线程。耗时计算如果直接写在槽函数里，窗口会卡住。"
    )

    st.header("和本项目的关系")
    st.write(
        "这个网站用 Streamlit 在浏览器里排版，Qt 则是在桌面窗口里排版，思路可以对照着看："
        "选择按钮、输入框都是控件，区别是一个跑在网页脚本里，一个跑在 C++ 事件循环里。"
        "学会 Qt 之后，可以把同样的「介绍 + 知识笔记」做成一个本地窗口程序。"
    )
