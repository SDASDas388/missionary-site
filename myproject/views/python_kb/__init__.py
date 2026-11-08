"""Python 知识。每一章一个文件，在下面的列表里按侧边栏顺序登记。"""

from views.python_kb.preface import render as render_preface
from views.python_kb.data_and_functions import render as render_data_and_functions
from views.python_kb.modules import render as render_modules
from views.python_kb.runtime import render as render_runtime
from views.python_kb.this_project import render as render_this_project

from views.knowledge import render_page

_CHAPTERS = [
    ("引言", render_preface),
    ("数据与函数", render_data_and_functions),
    ("模块与导入", render_modules),
    ("运行与环境", render_runtime),
    ("和本项目的关系", render_this_project),
]


def render() -> None:
    render_page("python", "Python 知识", _CHAPTERS)
