import streamlit as st
from pathlib import Path
from openai import OpenAI
from datetime import datetime
import json

APP_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = APP_DIR / "resource"
SESSIONS_DIR = APP_DIR / "sessions"

print("----------> 重新执行此文件 , 渲染展示页面")

#region 设置页面的配置项

st.set_page_config(
    #网站标题
    page_title="missionary星球",
    #网站图标
    page_icon="🤖",
    #控制网页布局
    layout="wide",
    #控制侧边栏的状态
    initial_sidebar_state="expanded",
    #右上角的菜单点击跳转内容
    menu_items={
        'About': "# 这将是missionary的个人网站"
    }
)


# 大标题
st.title("missionary助手")


# log
st.logo(str(RESOURCE_DIR / "logo.png"))
#endregion



#region 会话配置

# 生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# 保存会话信息函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 如果 sessions 目录不存在, 则创建
        SESSIONS_DIR.mkdir(exist_ok=True)

        # 保存会话数据
        with open(SESSIONS_DIR / f"{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

# 加载所有的会话列表信息
def load_sessions():
    session_list = []
    # 加载sessions目录下的文件
    if SESSIONS_DIR.exists():
        file_list = [path.name for path in SESSIONS_DIR.iterdir()]
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True) # 排序, 降序排列
    return session_list

# 加载指定的会话信息
def load_session(session_name):
    try:
        session_file = SESSIONS_DIR / f"{session_name}.json"
        if session_file.exists():
            # 读取会话数据
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败!")

# 删除会话信息函数
def delete_session(session_name):
    try:
        session_file = SESSIONS_DIR / f"{session_name}.json"
        if session_file.exists():
            session_file.unlink() # 删除文件
            # 如果删除的是当前会话, 则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败!")

#endregion





#region 大模型api

# 创建于AI大模型交互的客户端对象（DEEPSEEK_API_KEY环境变量的名字，值就是DeepSeek的API_KEY的 ）
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com")

#endregion



#region 系统提示词

system_prompt =  """
        你叫 %s，现在是为解决用户了解missionary的真实助理，请完全代入助理角色。
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合专业助理的方式对话
            7. 回复的内容, 要充分体现助理的性格特征
            8. 你主要的职责是为用户了解missionary所拥有的技能而服务的
        助理性格：
            - %s
        你必须严格遵守上述规则来回复用户。
    """



#endregion 

#region 初始化聊天信息



if "messages" not in st.session_state:
    st.session_state.messages = []

# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "missionary助理"
# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "资深项目经理"

# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


#endregion


#region 展示聊天信息
for message in st.session_state.messages:    # {"role": "user", "content": prompt}
    st.chat_message(message["role"]).write(message["content"])
#endregion 





#region 左侧的侧边栏

#with: streamlit中上下文管理器
with st.sidebar:

    #==============会话信息==================
    st.subheader("AI控制面板")

    # 新建会话
    if st.button("新建会话", width="stretch", icon="✏️"):
        save_session()

        # 2. 创建新的会话
        if st.session_state.messages: # 如果聊天信息非空, True; 否则,  False
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()  # 重新运行当前页面

    #==============会话历史==================
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
           # 加载会话信息
           # 三元运算符: 如果条件为真, 则返回第一个表达式的值; 否则, 返回第二个表达式的值 --> 语法: 值1 if 条件 else 值2,primary为高亮
           if st.button(session, width="stretch", icon="📄", key=f"load_{session}", type="primary" if session == st.session_state.current_session else "secondary"):
               load_session(session)
               st.rerun()
        with col2:
            # 删除会话信息
            if st.button("", width="stretch", icon="❌️", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()


    # =======================分割线=================
    st.divider()

    # ===============助理信息======================
    st.subheader("助理信息")
    # 昵称输入框
    nick_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    # 性格输入框
    nature = st.text_area("性格", placeholder="请输入性格", value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

#endregion








#region 聊天


# 消息输入框
prompt = st.chat_input("你可以问我关于missionary的所有信息")
if prompt: # 字符串会自动转换为布尔值, 如果字符串非空, 则为True; ""否则为False
    # user 代表大模型输入的消息
    st.chat_message("user").write(prompt)
    print("----------> 调用AI大模型, 提示词: ", prompt)

    # 保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content":prompt})

    # 调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-flash",
        # system 系统提示词
        # user 是用户提示词
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            # {"role": "user", "content": prompt},
            #存储记忆，将列表中的信息解包出来
            *st.session_state.messages
        ],
        # 是否是流式输出, False 为飞流式，True为流式输出
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 输出大模型返回的结果 (非流式输出的解析方式)
    # print("<---------- 大模型返回的结果: ", response.choices[0].message.content)
    # # assistant 代表机器人的消息
    # st.chat_message("assistant").write(response.choices[0].message.content)

    # 输出大模型返回的结果 (流式输出的解析方式)
    response_message = st.empty() # 创建一个空的组件, 用于展示大模型返回的结果

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)



    # 保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 保存会话信息
    save_session()

#endregion