from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = "NTron"
MONGO_COLLECTION = "Code_Snippets"

collection = MongoClient(MONGO_URI)[MONGO_DB][MONGO_COLLECTION]

def save_snippet(embedding, summary, code_text, file_path):
    document = {
        "Embedding": embedding,
        "Summary": summary,
        "Code Snippet": code_text,
        "Document ID": file_path
    }
    collection.insert_one(document)
    print(f"Saved snippet!")

def delete_snippet(file_path):
    result = collection.delete_many({"Document ID": file_path})

def search_snippet(query_embedding, top_k=5):
    result = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "Embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "default"
            }
        }
    ])
    return list(result)
