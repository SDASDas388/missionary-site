"""EDA 知识。每一章一个文件，在下面的列表里按侧边栏顺序登记。"""

from views.eda_kb.what import render as render_what
from views.eda_kb.schematic import render as render_schematic
from views.eda_kb.simulation import render as render_simulation
from views.eda_kb.pcb import render as render_pcb
from views.eda_kb.flow import render as render_flow
from views.eda_kb.this_project import render as render_this_project

from views.knowledge import render_page

_CHAPTERS = [
    ("是什么", render_what),
    ("原理图", render_schematic),
    ("仿真", render_simulation),
    ("PCB 与常见工具", render_pcb),
    ("设计流程", render_flow),
    ("和本项目的关系", render_this_project),
]


def render() -> None:
    render_page("eda", "EDA 知识", _CHAPTERS)
