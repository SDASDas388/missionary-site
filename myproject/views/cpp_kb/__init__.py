"""C++ 知识。每一章一个文件，在下面的列表里按侧边栏顺序登记。"""

from views.cpp_kb.preface import render as render_preface
from views.cpp_kb.simple_programming import render as render_simple_programming
from views.cpp_kb.function import render as render_function
from views.cpp_kb.classes import render as render_classes
from views.cpp_kb.this_project import render as render_this_project

from views.knowledge import render_page

_CHAPTERS = [
    ("前言", render_preface),
    ("C++语言简单程序设计", render_simple_programming),
    ("函数", render_function),
    ("类与标准库", render_classes),
    ("和本项目的关系", render_this_project),
]


def render() -> None:
    render_page("cpp", "C++ 知识", _CHAPTERS)
