import streamlit as st

#region 设置页面的配置项

st.set_page_config(
    #网站标题
    page_title="Ex-stream-ly Cool App",
    #网站图标
    page_icon="🧊",
    #控制网页布局
    layout="wide",
    #控制侧边栏的状态
    initial_sidebar_state="expanded",
    #右上角的菜单点击跳转内容
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 这将是missionary的个人网站"
    }
)

#endregion




# region 标题
# 大标题
st.title("王先生的空间站")

#一级标题
st.header("一级标题")

#二级标题
st.subheader("二级标题")

#endregion



# region 段落文字

st.write("我性格踏实稳重、积极好学，具备较强的自主学习能力和问题排查能力。平时做事认真细致，逻辑性强，遇到问题能够独立思考、耐心排查并总结经验。在技术方面，我熟悉 Python 基础开发、接口调用以及常见的程序调试方法，能够独立完成简单项目的开发与部署。")
st.write("工作学习中我注重效率与细节，善于复盘优化，具备良好的执行力与团队协作意识。未来我希望继续深耕技术，不断提升自己的专业能力，持续学习、稳步进步。")

#endregion

#region 图片

st.image("./resource/cc.jpg")

#endregion

#region 音频

st.audio("resource/maobuyi.mp3", format="audio/mp3")

#endregion

#region 视频
st.video("resource/news.mp4")
#endregion


#region Logo
st.logo("resource/logo.png")
#endregion

#region 表格
student_data = {
    "姓名": ["王林", "李慕婉", "贝罗", "莫厉海", "石萧"],
    "学号": ["20260001", "20260002", "20260003", "20260004", "20260005"],
    "语文": [98, 90, 59, 29, 80],
    "数学": [88, 78, 65, 70, 39],
    "英语": [99, 89, 87, 59, 62],
    "总分": [285, 257, 211, 158, 181]
}
st.table(student_data)

#endregion

# region 输入框

# 普通输入框
name = st.text_input("请输入姓名")
st.write(f"您输入的姓名为: {name}")

# 密码输入框
password = st.text_input("请输入密码", type="password")
st.write(f"您输入的密码为: {password}")

#endregion

# region 单选按钮

gender = st.radio("请输入您的性别", ["男", "女", "未知"], index=2)
st.write(f"您的性别为: {gender}")
#endregion