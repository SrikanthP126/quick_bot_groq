import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Streamlit UI Setup
st.title("💬 Groq AI Chatbot")

# Sidebar for API Key Entry
api_key = st.sidebar.text_input("🔑 Enter Groq API Key", value=GROQ_API_KEY, type="password")

if not api_key:
    st.warning("⚠️ Please enter a valid Groq API key.")
    st.stop()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input field for user
user_input = st.text_input("Type your message:", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # API Call to Groq
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": st.session_state.messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        assistant_message = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(assistant_message)
    else:
        st.error(f"❌ Error: {response.json()}")

