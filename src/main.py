import os
import streamlit as st
import ollama
from chat_memory import initialize_chat, add_user_message, format_chat_history
from pdf_loader import load_documents
from retrieval import create_document_chunks, build_faiss_index, retrieve_similar_chunks
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
    
    # Retrieve similar chunks
    similar_chunks = retrieve_similar_chunks(user_input, index, chunk_texts)
    context = "\n\n".join(similar_chunks)
    
    # Construct a full prompt for the model
    prompt = f"{format_chat_history()}\n\nRelevant Info:\n{context}\n\nUser: {user_input}\nAssistant:"
    
    #Generate response using the model (OLLAMA)
    response = ollama.chat(model = MODEL, messages=[{"role": "system", "content": prompt}])
    response_text = response["message"]["content"]
        
    add_user_message("assistant", response_text)
    st.chat_message("assistant").write(response_text)