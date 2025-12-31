import google.generativeai as genai
import streamlit as st

st.title("Gemini ChatGPT-like Clone")

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize model
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel("gemini-2.5-flash")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert history to Gemini format
    gemini_history = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [m["content"]]})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        chat = st.session_state.model.start_chat(history=gemini_history[:-1])
        response = chat.send_message(prompt)

        response_text = response.text
        response_placeholder.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
