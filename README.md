# High-Performance Vector Database

A scalable, high-performance vector database optimized for efficient storage, indexing, and retrieval of high-dimensional vectors. Supports Approximate Nearest Neighbor (ANN) search, metadata filtering, and hybrid search capabilities.

## Features

- Multi-modal vector support (text, images)
- Real-time vector indexing and search
- Metadata filtering
- Hybrid search capabilities
- GPU acceleration support
- Distributed architecture ready

## Architecture

The system consists of two main components:

1. **Vector Database Core (Rust)**
   - Efficient vector storage and indexing
   - ANN search implementation
   - Real-time updates
   
2. **Embedding Service (Python)**
   - Text embedding generation using SentenceTransformers
   - Image embedding generation using ViT
   - REST API for embedding generation

## Prerequisites

- Docker and Docker Compose
- NVIDIA GPU (optional, for faster embedding generation)
- NVIDIA Container Toolkit (if using GPU)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vector-db-project.git
   cd vector-db-project
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. The following services will be available:
   - Vector Database: http://localhost:8001
   - Embedding Service: http://localhost:8000

## API Usage

### Generate Text Embeddings

```bash
curl -X POST "http://localhost:8000/embed/text" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text here"}'
```

### Generate Image Embeddings

```bash
curl -X POST "http://localhost:8000/embed/image" \
     -F "file=@path/to/your/image.jpg"
```

### Vector Database Operations

The vector database exposes a REST API for:
- Vector insertion
- Nearest neighbor search
- Metadata filtering
- Vector deletion

## Development

### Building from Source

1. Rust Core:
   ```bash
   cd backend/rust-core
   cargo build --release
   ```

2. Python Embedding Service:
   ```bash
   cd backend/python-ml
   pip install -r requirements.txt
   python embedding_service.py
   ```

## Testing

Run the test suite:

```bash
# Rust tests
cd backend/rust-core
cargo test

# Python tests
cd backend/python-ml
pytest
```

## Performance

The system is optimized for:
- Low latency vector search
- Efficient memory usage
- GPU acceleration for embedding generation
- Horizontal scalability

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 