"""Qt 知识。每一章一个文件，在下面的列表里按侧边栏顺序登记。"""

from views.qt_kb.what import render as render_what
from views.qt_kb.signals import render as render_signals
from views.qt_kb.widgets import render as render_widgets
from views.qt_kb.event_loop import render as render_event_loop
from views.qt_kb.this_project import render as render_this_project

from views.knowledge import render_page

_CHAPTERS = [
    ("是什么", render_what),
    ("信号与槽", render_signals),
    ("控件与布局", render_widgets),
    ("事件循环", render_event_loop),
    ("和本项目的关系", render_this_project),
]


def render() -> None:
    render_page("qt", "Qt 知识", _CHAPTERS)
