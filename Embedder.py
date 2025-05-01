import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/v1/embeddings"  # Placeholder
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_embedding(text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": "text-embedding-ada-002",  # Update model if needed
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        embedding = response.json()['data'][0]['embedding']
        return embedding
    else:
        print("Error generating embedding:", response.text)
        return None

print(get_embedding("Hello, world!")) 