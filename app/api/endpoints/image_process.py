from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
from app.services.image_services import (
    resize_images, normalize_images, crop_images, rotate_flip_images,
    adjust_color_images, reduce_noise_images, remove_background_images
)
import os

router = APIRouter()

@router.post("/resize")
async def resize_endpoint(images: List[UploadFile] = File(...), width: int = 256, height: int = 256):
    filepaths = await resize_images(images, width, height)
    return {"message": "Images resized successfully", "filepaths": filepaths}

@router.post("/normalize")
async def normalize_endpoint(images: List[UploadFile] = File(...)):
    filepaths = await normalize_images(images)
    return {"message": "Images normalized successfully", "filepaths": filepaths}

@router.post("/crop")
async def crop_endpoint(images: List[UploadFile] = File(...), x: int = 0, y: int = 0, width: int = 256, height: int = 256):
    filepaths = await crop_images(images, x, y, width, height)
    return {"message": "Images cropped successfully", "filepaths": filepaths}

@router.post("/rotate-flip")
async def rotate_flip_endpoint(images: List[UploadFile] = File(...), rotate_angle: int = 0, flip_code: int = 1):
    filepaths = await rotate_flip_images(images, rotate_angle, flip_code)
    return {"message": "Images rotated/flipped successfully", "filepaths": filepaths}

@router.post("/color-adjust")
async def color_adjust_endpoint(images: List[UploadFile] = File(...), brightness: int = 0, contrast: int = 0, saturation: int = 0):
    filepaths = await adjust_color_images(images, brightness, contrast, saturation)
    return {"message": "Images color-adjusted successfully", "filepaths": filepaths}

@router.post("/noise-reduction")
async def noise_reduction_endpoint(images: List[UploadFile] = File(...)):
    filepaths = await reduce_noise_images(images)
    return {"message": "Images noise-reduced successfully", "filepaths": filepaths}

@router.post("/background-removal")
async def background_removal_endpoint(images: List[UploadFile] = File(...)):
    filepaths = await remove_background_images(images)
    return {"message": "Backgrounds removed from images successfully", "filepaths": filepaths}

@router.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join("/tmp/processed_images", filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type='image/png', filename=filename)
    return {"error": "File not found"}
