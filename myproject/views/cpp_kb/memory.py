"""C++ 知识：类型与内存"""

import streamlit as st


def render() -> None:
    st.write(
        "变量有明确类型，int、double、std::string 不能随便混用。对象活在栈上或堆上，"
        "堆上的资源需要有人负责释放。现代写法用 RAII：对象构造时取得资源，析构时自动归还，"
        "例如 std::vector 和 std::unique_ptr。"
    )
