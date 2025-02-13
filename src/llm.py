import ollama

MODEL = "llama3"

def generate_answer(context, question, chat_history):
    """
    Uses Llama 3 via Ollama to generate an AI answer based on retrieved document context.
    """
    prompt = f"""
    You are a helpful AI assistant. Use the following context to answer the question accurately.

    Chat History:
    {chat_history}

    Relevant Info:
    {context}

    User: {question}
    Assistant:
    """
    response = ollama.chat(model=MODEL, messages=[{"role": "system", "content": prompt}])
    return response["message"]["content"]
