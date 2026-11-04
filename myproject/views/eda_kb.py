import streamlit as st

from views.chapters import select_chapter

CHAPTERS = [
    "是什么",
    "原理图",
    "仿真",
    "PCB 与常见工具",
    "设计流程",
    "和本项目的关系",
]


def _what() -> None:
    st.write(
        "EDA 在这里指电子设计自动化（Electronic Design Automation）。"
        "它用软件完成电路原理图、仿真、印制电路板（PCB）布局布线，"
        "让硬件设计可以在计算机上检查，再送到工厂制板。"
    )


def _schematic() -> None:
    st.write(
        "原理图用符号表示电阻、电容、芯片和连接关系，讲的是「谁和谁相连」，还不是物理位置。"
        "每个元件要有封装，封装描述它在板上的焊盘形状，后面才能落到 PCB。"
    )


def _simulation() -> None:
    st.write(
        "仿真是在制板之前用模型跑电路，看电压、电流和时序是否合理。"
        "模拟电路常用 SPICE 一类工具，数字电路还会看逻辑是否按预期翻转。"
        "仿真通过不能代替实板测试，但能提前发现明显接错和参数问题。"
    )


def _pcb() -> None:
    st.write(
        "PCB 设计把原理图变成铜箔走线、过孔和器件摆放，同时要考虑线宽、间距、地层和干扰。"
        "入门常用 KiCad，工业场景里常见 Altium Designer。两者都覆盖原理图捕获和 PCB 布局。"
    )


def _flow() -> None:
    st.write(
        "一条常见路径是：需求与框图，画原理图，给元件指定封装，做必要的仿真，"
        "再绘制 PCB、布线并检查设计规则，最后导出制板文件并焊接调试。"
        "调试时用万用表和示波器对照原理图，确认软件读到的信号和硬件一致。"
    )


def _this_project() -> None:
    st.write(
        "Python、C++ 和 Qt 解决的是软件与界面，EDA 解决的是这些程序要对话的电路。"
        "把四块放在同一个网站里，是为了把「写程序」和「看电路」连成一条学习线："
        "接口、界面和板级信号可以对照着记。"
    )


_BODY = {
    "是什么": _what,
    "原理图": _schematic,
    "仿真": _simulation,
    "PCB 与常见工具": _pcb,
    "设计流程": _flow,
    "和本项目的关系": _this_project,
}


def render() -> None:
    chapter = select_chapter("eda", CHAPTERS, page_title="EDA 知识")
    st.title("EDA 知识")
    st.header(chapter)
    _BODY[chapter]()
