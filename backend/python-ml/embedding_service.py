from typing import Union, List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import ViTFeatureExtractor, ViTModel
from PIL import Image
import torch
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_TEXT_LENGTH = 512
MAX_IMAGE_SIZE = (1024, 1024)  # Maximum dimensions
SUPPORTED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

class EmbeddingService:
    def __init__(self):
        try:
            # Initialize text embedding model
            self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize image embedding model
            self.image_feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
            self.image_model = ViTModel.from_pretrained('google/vit-base-patch16-224')
            
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.image_model.to(self.device)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize models: {str(e)}")

    async def get_text_embedding(self, text: str) -> List[float]:
        if not text.strip():
            raise ValueError("Empty text input")
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters")
        
        try:
            embedding = self.text_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            raise RuntimeError(f"Text embedding generation failed: {str(e)}")

    async def get_image_embedding(self, image_data: bytes) -> List[float]:
        try:
            # Validate image format
            image = Image.open(io.BytesIO(image_data))
            if image.format.upper() not in {'JPEG', 'PNG', 'WEBP'}:
                raise ValueError("Unsupported image format")
            
            # Resize if too large
            if image.size[0] > MAX_IMAGE_SIZE[0] or image.size[1] > MAX_IMAGE_SIZE[1]:
                image.thumbnail(MAX_IMAGE_SIZE)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            inputs = self.image_feature_extractor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.image_model(**inputs)
                embedding = outputs.pooler_output[0]
            
            return embedding.cpu().numpy().tolist()
        except Exception as e:
            raise RuntimeError(f"Image embedding generation failed: {str(e)}")

service = EmbeddingService()

@app.post("/embed/text")
async def embed_text(text: str) -> Dict[str, List[float]]:
    try:
        embedding = await service.get_text_embedding(text)
        return {"embedding": embedding}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed/image")
async def embed_image(file: UploadFile = File(...)) -> Dict[str, List[float]]:
    if not file.content_type in SUPPORTED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image format")
    
    try:
        image_data = await file.read()
        if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="Image file too large")
        
        embedding = await service.get_image_embedding(image_data)
        return {"embedding": embedding}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models": {
            "text": "all-MiniLM-L6-v2",
            "image": "google/vit-base-patch16-224"
        },
        "device": str(service.device)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 