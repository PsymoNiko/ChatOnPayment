"""
Basement Microservice - FastAPI Application

Provides file upload and base model functionality.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import uuid
from PIL import Image
from io import BytesIO

app = FastAPI(title="Basement Service", version="0.1.0")


class FileUploadResponse(BaseModel):
    """File upload response model."""
    file_id: str
    file_name: str
    file_url: str
    thumbnail_url: Optional[str] = None
    file_tags: Optional[str] = None
    bucket_name: str
    created_at: str


class CategoryRequest(BaseModel):
    """Category request model."""
    title: str
    parent_id: Optional[str] = None
    file_tags: Optional[str] = None


class CategoryResponse(BaseModel):
    """Category response model."""
    category_id: str
    title: str
    slug: str
    level: int
    parent_id: Optional[str] = None
    file_url: Optional[str] = None
    created_at: str


# In-memory storage for demonstration (replace with database in production)
uploaded_files = {}
categories = {}


def make_thumbnail(image_data: bytes, size=(300, 300)) -> bytes:
    """Create a thumbnail from image data."""
    try:
        img = Image.open(BytesIO(image_data))
        img = img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=100)
        thumb_io.seek(0)
        return thumb_io.getvalue()
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None


@app.get("/healthz")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


@app.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    file_tags: Optional[str] = None,
    bucket_name: str = "chat-bucket"
):
    """
    Upload a file and optionally create a thumbnail.
    
    For SVG files, the original file is used as thumbnail.
    For other image types, a thumbnail is generated.
    """
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1].lower()
    
    # Read file content
    file_content = await file.read()
    
    # Store file (in-memory for now)
    file_url = f"/files/{file_id}.{file_extension}"
    thumbnail_url = file_url
    
    # Create thumbnail for non-SVG images
    if file_extension != 'svg' and file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        thumbnail_data = make_thumbnail(file_content)
        if thumbnail_data:
            thumbnail_url = f"/files/{file_id}_thumbnail.png"
    
    uploaded_files[file_id] = {
        "file_name": file.filename,
        "file_url": file_url,
        "thumbnail_url": thumbnail_url,
        "file_tags": file_tags,
        "bucket_name": bucket_name,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return FileUploadResponse(
        file_id=file_id,
        file_name=file.filename,
        file_url=file_url,
        thumbnail_url=thumbnail_url,
        file_tags=file_tags,
        bucket_name=bucket_name,
        created_at=uploaded_files[file_id]["created_at"]
    )


@app.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about an uploaded file."""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    return uploaded_files[file_id]


@app.post("/categories", response_model=CategoryResponse)
async def create_category(category: CategoryRequest):
    """Create a new category."""
    category_id = str(uuid.uuid4())
    slug = category.title.lower().replace(' ', '-')
    
    # Determine level based on parent
    level = 0
    if category.parent_id and category.parent_id in categories:
        level = categories[category.parent_id]["level"] + 1
    
    categories[category_id] = {
        "title": category.title,
        "slug": slug,
        "level": level,
        "parent_id": category.parent_id,
        "file_url": None,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return CategoryResponse(
        category_id=category_id,
        title=category.title,
        slug=slug,
        level=level,
        parent_id=category.parent_id,
        file_url=None,
        created_at=categories[category_id]["created_at"]
    )


@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str):
    """Get a category by ID."""
    if category_id not in categories:
        raise HTTPException(status_code=404, detail="Category not found")
    
    cat = categories[category_id]
    return CategoryResponse(
        category_id=category_id,
        title=cat["title"],
        slug=cat["slug"],
        level=cat["level"],
        parent_id=cat["parent_id"],
        file_url=cat["file_url"],
        created_at=cat["created_at"]
    )


@app.get("/categories")
async def list_categories():
    """List all categories."""
    return [
        {
            "category_id": cat_id,
            **cat
        }
        for cat_id, cat in categories.items()
    ]
