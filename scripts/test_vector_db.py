import requests
import json
from typing import List, Dict
import numpy as np

class VectorDBClient:
    def __init__(self, embedding_url: str = "http://localhost:8000", db_url: str = "http://localhost:8001"):
        self.embedding_url = embedding_url
        self.db_url = db_url

    def get_text_embedding(self, text: str) -> List[float]:
        response = requests.post(
            f"{self.embedding_url}/embed/text",
            json={"text": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def insert_vector(self, id: str, embedding: List[float], metadata: Dict[str, str]):
        response = requests.post(
            f"{self.db_url}/vector",
            json={
                "id": id,
                "embedding": embedding,
                "metadata": metadata
            }
        )
        response.raise_for_status()
        return response.text

    def search_similar(self, query_vector: List[float], k: int = 5):
        response = requests.post(
            f"{self.db_url}/search",
            json={
                "vector": query_vector,
                "k": k
            }
        )
        response.raise_for_status()
        return response.json()["results"]

def main():
    client = VectorDBClient()

    # Test data
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "A lazy dog sleeps in the sun",
        "The brown fox is quick and clever",
        "Dogs are man's best friend",
        "Foxes are wild animals"
    ]

    print("1. Getting embeddings for test texts...")
    embeddings = []
    for i, text in enumerate(texts):
        print(f"\nProcessing text {i + 1}: {text}")
        embedding = client.get_text_embedding(text)
        embeddings.append(embedding)
        print(f"Embedding dimension: {len(embedding)}")
        
        # Store in vector database
        metadata = {"type": "text", "content": text}
        client.insert_vector(f"text_{i}", embedding, metadata)
        print(f"Stored in database with ID: text_{i}")

    # Test similarity search
    print("\n2. Testing similarity search...")
    query_text = "A quick fox"
    print(f"\nSearching for similar texts to: '{query_text}'")
    
    query_embedding = client.get_text_embedding(query_text)
    results = client.search_similar(query_embedding, k=3)
    
    print("\nTop 3 similar texts:")
    for i, (id, similarity) in enumerate(results):
        print(f"{i + 1}. Text ID: {id}, Similarity: {similarity:.4f}")

if __name__ == "__main__":
    main() 