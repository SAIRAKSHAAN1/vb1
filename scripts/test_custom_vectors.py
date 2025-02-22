import requests
import numpy as np

def normalize_vector(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

# Test vectors (3D for simplicity)
vectors = [
    normalize_vector(np.array([1.0, 0.0, 0.0])),  # Vector pointing in x direction
    normalize_vector(np.array([0.0, 1.0, 0.0])),  # Vector pointing in y direction
    normalize_vector(np.array([0.0, 0.0, 1.0])),  # Vector pointing in z direction
    normalize_vector(np.array([1.0, 1.0, 0.0])),  # 45 degrees between x and y
    normalize_vector(np.array([1.0, 1.0, 1.0])),  # Equal in all directions
]

# Insert vectors into the database
print("Inserting test vectors...")
for i, vec in enumerate(vectors):
    response = requests.post(
        "http://localhost:8001/vector",
        json={
            "id": f"vec_{i}",
            "embedding": vec.tolist(),
            "metadata": {"type": "test_vector", "description": f"Test vector {i}"}
        }
    )
    print(f"Inserted vector {i}: {vec.tolist()}")
    response.raise_for_status()

# Test queries
test_queries = [
    ([1.0, 0.1, 0.0], "Almost x direction"),
    ([0.7, 0.7, 0.0], "Between x and y"),
    ([0.577, 0.577, 0.577], "Equal in all directions"),
]

print("\nTesting similarity search...")
for query_vec, description in test_queries:
    query_vec = normalize_vector(np.array(query_vec)).tolist()
    print(f"\nQuery: {description}")
    print(f"Vector: {query_vec}")
    
    response = requests.post(
        "http://localhost:8001/search",
        json={
            "vector": query_vec,
            "k": 3
        }
    )
    response.raise_for_status()
    results = response.json()["results"]
    
    print("Top 3 similar vectors:")
    for i, (id, similarity) in enumerate(results):
        print(f"{i + 1}. Vector ID: {id}, Similarity: {similarity:.4f}")

if __name__ == "__main__":
    pass 