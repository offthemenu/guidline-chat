import streamlit as st

def initialize_chat():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "system",
             "content": "Hello! I am your guideline assistant. How can I help you today?"}
        ]

def add_user_message(role, content):
    st.session_state["chat_history"].append({"role": role, "content": content})
    
def format_chat_history():
    return "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["chat_history"]]) # Return the formatted chat history