#api_key = sk-proj-Y5vJCTMDFvPxLz1epO5YT3BlbkFJV52J1W0NVH9lZU3Grk5I

import streamlit as st
import openai
from datetime import datetime

def ask_gpt(prompt, model, apikey):
    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model=model,
        messages=prompt)
    gptResponse = response.choices[0].message.content
    return gptResponse

def main():

    st.set_page_config(
        page_title="채팅 비서 프로그램", layout="wide")

    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "OPEN_API" not in st.session_state:
        st.session_state["OPEN_API"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"system", "content":"You are a thoughtful assistant. Respond to all input 25 words and answer in Korean."}]
    if "Question" not in st.session_state:
        st.session_state["Question"] = False

    st.header("채팅 비서 프로그램")

    st.markdown("---")

    with st.sidebar:
        st.session_state["OPEN_API"] = st.text_input(label="OPEN API 키", placeholder="Enter Your API Key", value="", type="password")
        st.markdown("---")

        model = st.radio(label="GPT모델", options=["gpt-3.5-turbo", "gpt-4"])
                         
        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role":"system", "content":"You are a thoughtful assistant. Respond to all input 25 words and answer in Korean."}]
            st.session_state["check_reset"] = True

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("질문하기")
        question = st.session_state["Question"] = st.text_input(label="", placeholder="질문을 입력하세요", value="")
        if question:
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+[("user", now, question)]
            st.session_state["messages"] = st.session_state["messages"]+[{"role":"user", "content":question}]
    with col2:
        st.subheader("질문/답변")
        if question:
            response = ask_gpt(st.session_state["messages"], model, st.session_state["OPEN_API"])
            st.session_state["messages"] = st.session_state["messages"]+[{"role":"system", "content":response}]
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+[("bot", now, response)]
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")

if __name__=="__main__":
    main()