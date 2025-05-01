import ast
from Summarizer import summarize_code
from Embedder2 import embed_text
from DB_Manager import save_snippet, delete_snippet

def process_file(filepath):
    delete_snippet(filepath)
    print(f"Processing {filepath}")
    with open(filepath, "r", encoding="utf-8") as file:
        code = file.read()
    
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            function_code = ast.get_source_segment(code, node)
            print(f"Found Function: {function_name}")
            print(function_code)
            print("-" * 40)
            summary = summarize_code(function_code)
            print(f"Summary: {summary}")
            embedding = embed_text(summary)
            save_snippet(embedding, summary, function_code, filepath)

        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_code = ast.get_source_segment(code, node)
            print(f"Found Class: {class_name}")
            print(class_code)
            print("-" * 40)
            summary = summarize_code(class_code)
            print(f"Summary: {summary}")
            print(f"Summary: {summary}")
            embedding = embed_text(summary)
            save_snippet(embedding, summary, class_code, filepath)
