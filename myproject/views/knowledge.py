"""四门知识页共用的页面外壳。章节正文各自放在独立文件里。"""

from collections.abc import Callable

import streamlit as st

from views.chapters import select_chapter


def render_page(
    page_key: str,
    page_title: str,
    chapters: list[tuple[str, Callable[[], None]]],
) -> None:
    """画出侧边栏和标题，并调用当前章节的 render。

    chapters 是 (章节名, 渲染函数) 的列表，顺序就是侧边栏顺序。
    新增一章时，写好那个文件，再往对应知识包的列表里加一项。
    """
    names = [name for name, _render in chapters]
    selected = select_chapter(page_key, names, page_title=page_title)
    st.title(page_title)
    st.header(selected)
    dict(chapters)[selected]()
