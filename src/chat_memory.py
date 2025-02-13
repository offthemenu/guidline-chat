import streamlit as st

def initialize_chat():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "system",
             "content": "Hello! I am your guideline assistant. How can I help you today?"}
        ]

def add_user_message(role, content):
    '''
    Add a user message to the chat history
    '''
    st.session_state["chat_history"].append({"role": role, "content": content})

def display_chat():
    '''
    Displays chat history without additional formatting
    '''

    for message in st.session_state["chat_history"]:
        if message["role"] == "user":
            st.chat_message("user").write(f"**User:** {message['content']}")
        else:
            st.chat_message("assistant").write(f"**Assistant:** {message['content']}")