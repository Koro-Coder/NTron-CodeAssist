import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def chat_with_groq(user_chat_history):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "messages": user_chat_history,
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",  # Choose a model from GROQ
        "temperature": 0.2,
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content'].strip()
        return reply
    else:
        print("Error calling LLM:", response.text)
        return "Something Went Wrong!"
