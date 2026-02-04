import streamlit as st
import google.generativeai as genai

# 1. 页面配置（手机适配）
st.set_page_config(page_title="AI 助手", layout="centered")

# 2. 设置你的 API Key (从 AI Studio 获取)
# 提示：正式发布时建议使用 st.secrets 管理密钥
API_KEY = "AIzaSyADEEGBcaO9r3_zGHsXLSX6I54MUHk4tes"
genai.configure(api_key=API_KEY)

st.title("🎨 我的 AI 灵感助手")
st.caption("基于 Gemini 3 Flash | 手机专属版")

# 3. 侧边栏设置
with st.sidebar:
    st.header("设置")
    model_name = st.selectbox("选择模型", ["gemini-3-flash", "gemini-3-pro-preview"])
    temperature = st.slider("创意程度", 0.0, 1.0, 0.7)

# 4. 聊天记录初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 展示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 聊天输入框
if prompt := st.chat_input("说点什么..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用 Gemini 模型
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={"temperature": temperature}
            )
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"出错了: {str(e)}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
