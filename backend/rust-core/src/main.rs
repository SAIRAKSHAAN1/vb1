use actix_web::{web, App, HttpServer, Result, error::ErrorInternalServerError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use vector_db_core::{VectorDB, VectorDBError};
use std::sync::Arc;

#[derive(Deserialize)]
struct VectorInsert {
    id: String,
    embedding: Vec<f32>,
    metadata: HashMap<String, String>,
}

#[derive(Deserialize)]
struct SearchQuery {
    vector: Vec<f32>,
    k: usize,
}

#[derive(Serialize)]
struct SearchResult {
    results: Vec<(String, f32)>,
}

struct AppState {
    db: Arc<VectorDB>,
}

async fn insert_vector(
    state: web::Data<AppState>,
    payload: web::Json<VectorInsert>,
) -> Result<&'static str> {
    state
        .db
        .insert(
            payload.id.clone(),
            payload.embedding.clone(),
            payload.metadata.clone(),
        )
        .await
        .map_err(ErrorInternalServerError)?;
    Ok("Vector inserted successfully")
}

async fn search_nearest(
    state: web::Data<AppState>,
    query: web::Json<SearchQuery>,
) -> Result<web::Json<SearchResult>> {
    let results = state
        .db
        .search_nearest(query.vector.clone(), query.k)
        .await
        .map_err(ErrorInternalServerError)?;
    Ok(web::Json(SearchResult { results }))
}

async fn delete_vector(
    state: web::Data<AppState>,
    id: web::Path<String>,
) -> Result<&'static str> {
    state
        .db
        .delete(&id)
        .await
        .map_err(ErrorInternalServerError)?;
    Ok("Vector deleted successfully")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let vector_db = Arc::new(VectorDB::new(768)); // Standard dimension for many embedding models
    let state = web::Data::new(AppState { db: vector_db });

    println!("Starting vector database server on port 8001");
    
    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .route("/vector", web::post().to(insert_vector))
            .route("/search", web::post().to(search_nearest))
            .route("/vector/{id}", web::delete().to(delete_vector))
    })
    .bind("0.0.0.0:8001")?
    .run()
    .await
} 