"""C++ 知识：类与标准库"""

import streamlit as st


def render() -> None:
    st.write(
        "类把数据和操作包在一起。公有成员给外部用，私有成员留在内部。"
        "STL 提供 vector、string、map 等容器和算法，多数业务代码优先用它们，而不是手写数组。"
    )
