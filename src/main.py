import os
import streamlit as st
import ollama
from chat_memory import initialize_chat, add_user_message, format_chat_history
from pdf_loader import load_documents
from retrieval import create_document_chunks, build_faiss_index, retrieve_similar_chunks
from llm import generate_answer
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*Beta.*")
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

MODEL = "llama3"  # Change model if needed

# Streamlit UI setup
st.set_page_config(layout="wide")
st.title("Guideline Assistant")

initialize_chat()

# File uploader
uploaded_file = st.file_uploader("Upload Documents", accept_multiple_files=True, type=["pdf", "txt", "yaml"])

if uploaded_file:
    doc_folder = "docs"
    os.makedirs(doc_folder, exist_ok=True)
    
    # Save the uploaded files
    for file in uploaded_file:
        with open(os.path.join(doc_folder, file.name), "wb") as f:
            f.write(file.getbuffer())
            
    st.success("Documents uploaded successfully!")
    
    # Process documents
    docs = load_documents(doc_folder)
    doc_chunks = create_document_chunks(docs)
    index, chunk_texts = build_faiss_index(doc_chunks)
    
    st.success(f"Loaded {len(doc_chunks)} document chunks.")
    
# Display chat history
for message in st.session_state["chat_history"]:
    st.chat_message(message["role"]).write(message["content"])

# User input
user_input = st.chat_input("Ask a question...")

if user_input:
    add_user_message("user", user_input)
    
    # Ensure documents were uploaded before retrieving
    if "index" in locals() and "chunk_texts" in locals():
        # Retrieve similar chunks
        similar_chunks = retrieve_similar_chunks(user_input, index, chunk_texts)
        context = "\n\n".join(similar_chunks)
    else:
        context = "No documents have been uploaded. Please upload relevant guidelines."

    # Generate AI response using Llama 3
    response_text = generate_answer(context, user_input, format_chat_history())

    # Store & display assistant response
    add_user_message("assistant", response_text)
    st.chat_message("assistant").write(response_text)