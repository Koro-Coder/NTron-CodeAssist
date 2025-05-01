import requests
import json

def embed_text(text: str, model: str = "nomic-embed-text") -> list[float]:
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": model,
        "prompt": text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["embedding"]
