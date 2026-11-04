import streamlit as st


def _choose_chapter(memory_key: str, name: str) -> None:
    st.session_state[memory_key] = name


def select_chapter(page_key: str, chapters: list[str], *, page_title: str) -> str:
    """在侧边栏列出本章节，并返回当前选中的章节名。

    选中项记在单独的 session state 里，切换顶部页面后再回来仍然停在这一章。
    新增章节时，把名字加进调用处的列表即可。
    """
    memory_key = f"chapter_memory_{page_key}"
    if st.session_state.get(memory_key) not in chapters:
        st.session_state[memory_key] = chapters[0]

    selected = st.session_state[memory_key]
    with st.sidebar:
        st.subheader(page_title)
        for name in chapters:
            st.button(
                name,
                key=f"chapter_btn_{page_key}_{name}",
                width="stretch",
                type="primary" if name == selected else "secondary",
                on_click=_choose_chapter,
                args=(memory_key, name),
            )
    return selected
