import requests
import ollama

# llama3 only supports local usage. We'll need to think about using a free model on huggingface that can support cloud deployment
# first, let's try using ngrok to use ollama and keep it running on my mac mini

MODEL = "llama3"
OLLAMA_SERVER_URL = "https://de99-112-220-73-130.ngrok-free.app"

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
    response = requests.post(
        OLLAMA_SERVER_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "system", "content": prompt}]
        }
    )
    return response.json()["message"]["content"]
