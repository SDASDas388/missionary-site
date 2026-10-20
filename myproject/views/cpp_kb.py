import streamlit as st


def render():
    st.title("C++ 知识")

    st.header("是什么")
    st.write(
        "C++ 是在 C 的基础上加上类、模板和更严格类型系统的编译型语言。"
        "源文件要先编译成目标文件，再链接成可执行程序，运行时不再依赖解释器。"
        "它既能写贴近硬件的程序，也是 Qt 桌面应用的常用语言。"
    )

    st.header("核心概念")
    st.subheader("编译与链接")
    st.write(
        "编译器把 .cpp 翻译成机器码，链接器再把你的代码和标准库拼成一个程序。"
        "头文件负责声明，源文件负责实现。改完代码必须重新编译，程序才会更新。"
    )
    st.subheader("类型与内存")
    st.write(
        "变量有明确类型，int、double、std::string 不能随便混用。对象活在栈上或堆上，"
        "堆上的资源需要有人负责释放。现代写法用 RAII：对象构造时取得资源，析构时自动归还，"
        "例如 std::vector 和 std::unique_ptr。"
    )
    st.subheader("类与标准库")
    st.write(
        "类把数据和操作包在一起。公有成员给外部用，私有成员留在内部。"
        "STL 提供 vector、string、map 等容器和算法，多数业务代码优先用它们，而不是手写数组。"
    )

    st.header("和本项目的关系")
    st.write(
        "本站本身用 Python 编写，C++ 是旁边的一条学习线。"
        "理解编译、类型和对象生命周期之后，再看 Qt 的控件和信号槽会轻松很多："
        "Qt 的窗口、按钮本质上都是 C++ 对象。"
    )
