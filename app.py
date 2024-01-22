
import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Funtion to load Gemini model and Gemini pro molde and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_icon="🤖",
                   page_title="Gemini pro Q&A demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []


input = st.chat_input("Input:-", key="input")

if input:
    resp_op = get_gemini_response(input)

    # Add user query and response to session chat history
    st.session_state['chat_history'].append(('You', input))

    for chunk in resp_op:
        st.session_state['chat_history'].append(('Bot', chunk.text))


for role, text in st.session_state['chat_history']:
    if role == "Bot":
        with st.chat_message("assistant", avatar="🤖"):
            st.write(f"{text}")
    else:
        message = st.chat_message("user", avatar="🧑")
        message.write(f"{text}")
