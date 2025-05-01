import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_code(code_snippet):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an expert code assistant. When given a code snippet—whether a class, function, or module—summarize it in 1–3 sentences. Focus on:\n\n• Its overall purpose and functionality\n• Key components (e.g. main classes, functions, data structures)\n• Any notable algorithms or design patterns used\n\nWrite concise, technical summaries that help developers quickly find and understand relevant code."
            },
            {
                "role": "user", 
                "content": code_snippet
            }
        ],
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",  # Choose a model from GROQ
        "temperature": 0.2,
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        summary = response.json()['choices'][0]['message']['content'].strip()
        return summary
    else:
        print("Error summarizing:", response.text)
        return "Summary unavailable"
