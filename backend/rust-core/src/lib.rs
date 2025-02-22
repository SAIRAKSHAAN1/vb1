use std::collections::HashMap;
use ndarray::{Array1, ArrayView1};
use serde::{Serialize, Deserialize};
use thiserror::Error;
use tokio::sync::RwLock;
use std::sync::Arc;

#[derive(Error, Debug)]
pub enum VectorDBError {
    #[error("Vector not found: {0}")]
    NotFound(String),
    #[error("Dimension mismatch: expected {expected}, got {got}")]
    DimensionMismatch { expected: usize, got: usize },
    #[error("Database error: {0}")]
    DatabaseError(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Vector {
    id: String,
    embedding: Vec<f32>,
    metadata: HashMap<String, String>,
}

pub struct VectorDB {
    vectors: Arc<RwLock<HashMap<String, Vector>>>,
    dimension: usize,
}

impl VectorDB {
    pub fn new(dimension: usize) -> Self {
        Self {
            vectors: Arc::new(RwLock::new(HashMap::new())),
            dimension,
        }
    }

    pub async fn insert(&self, id: String, embedding: Vec<f32>, metadata: HashMap<String, String>) -> Result<(), VectorDBError> {
        if embedding.len() != self.dimension {
            return Err(VectorDBError::DimensionMismatch {
                expected: self.dimension,
                got: embedding.len(),
            });
        }

        let vector = Vector {
            id: id.clone(),
            embedding,
            metadata,
        };

        let mut vectors = self.vectors.write().await;
        vectors.insert(id, vector);
        Ok(())
    }

    pub async fn search_nearest(&self, query: Vec<f32>, k: usize) -> Result<Vec<(String, f32)>, VectorDBError> {
        if query.len() != self.dimension {
            return Err(VectorDBError::DimensionMismatch {
                expected: self.dimension,
                got: query.len(),
            });
        }

        let vectors = self.vectors.read().await;
        let query = Array1::from(query);
        
        let mut distances: Vec<(String, f32)> = vectors
            .iter()
            .map(|(id, vector)| {
                let embedding = Array1::from(vector.embedding.clone());
                let distance = cosine_similarity(query.view(), embedding.view());
                (id.clone(), distance)
            })
            .collect();

        distances.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        Ok(distances.into_iter().take(k).collect())
    }

    pub async fn get(&self, id: &str) -> Result<Vector, VectorDBError> {
        let vectors = self.vectors.read().await;
        vectors
            .get(id)
            .cloned()
            .ok_or_else(|| VectorDBError::NotFound(id.to_string()))
    }

    pub async fn delete(&self, id: &str) -> Result<(), VectorDBError> {
        let mut vectors = self.vectors.write().await;
        vectors
            .remove(id)
            .ok_or_else(|| VectorDBError::NotFound(id.to_string()))?;
        Ok(())
    }
}

fn cosine_similarity(a: ArrayView1<f32>, b: ArrayView1<f32>) -> f32 {
    let dot_product = a.dot(&b);
    let norm_a = (a.dot(&a)).sqrt();
    let norm_b = (b.dot(&b)).sqrt();
    dot_product / (norm_a * norm_b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_vector_operations() {
        let db = VectorDB::new(3);
        
        // Test insertion
        let mut metadata = HashMap::new();
        metadata.insert("type".to_string(), "test".to_string());
        
        db.insert(
            "vec1".to_string(),
            vec![1.0, 0.0, 0.0],
            metadata.clone(),
        )
        .await
        .unwrap();

        // Test retrieval
        let vector = db.get("vec1").await.unwrap();
        assert_eq!(vector.embedding, vec![1.0, 0.0, 0.0]);

        // Test search
        let results = db.search_nearest(vec![1.0, 0.1, 0.0], 1).await.unwrap();
        assert_eq!(results[0].0, "vec1");
    }
} 