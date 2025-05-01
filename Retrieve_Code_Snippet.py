from DB_Manager import search_snippet
from Embedder2 import embed_text

def search_code_snippet(query, top_k = 3):
    embedding = embed_text(query)
    results = search_snippet(embedding, top_k)
    return results

search_code_snippet("Disjoint Set Union")