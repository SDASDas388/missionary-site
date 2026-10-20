# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI
import streamlit as st

# 创建于AI大模型交互的客户端对象（DEEPSEEK_API_KEY环境变量的名字，值就是DeepSeek的API_KEY的 ）
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com")

# 与AI大模型进行交互（）
response = client.chat.completions.create(
    model="deepseek-flash",
    # system 系统提示词
    # role 是用户提示词
    messages=[
        {"role": "system", "content": "你是王先生的助手，你的名字叫做小王，你能介绍关于王先生的各种技能"},
        {"role": "user", "content": "你是谁，你能帮我做什么"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

# 输出大模型返回的结果
print(response.choices[0].message.content)

#region 提示词大总结

#1. 给大模型设定角色与能力
#  例如： 你是一名经验丰富的高中历史老师， 擅长生动有趣的讲解复杂历史事件

#2. 明确核心请求与任务
#  例如： 请向一位高中生解释法国大革命爆发的主要原因

#3. 按步骤拆解复杂任务
#  例如：  请先概况背景，然后分政治，经济，思想三个方面阐述，每点配一个例子

#4. 指定风格与语气
#  例如：  请使用简介，口语，充满热情的语气（避免使用过于学术的术语）

#5. 明确要求输出格式
#  例如：  请严格按照如下结构输出

#6. 提供输入输出的是咧

#endregion