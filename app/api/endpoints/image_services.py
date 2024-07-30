from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from app.services.image_services import resize_images, normalize_image
from typing import List
import cv2 
import os 




router = APIRouter()



@router.post("/resize/")
async def resize_images_endpoint(width: int, height: int, files: List[UploadFile] = File(...)):
    try:
        size = (width, height)
        resized_images = await resize_images(size, files)
        return {"message": "Images resized successfully", "data": resized_images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/normalize-image/")
async def normalize_image_endpoint(files: List[UploadFile] = File(...)):
    try:
        normalized_image = await normalize_image(files)
        return JSONResponse(content={"normalized_image": normalized_image})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/download_image_normalized/{filename}")
async def download_image_normalized(filename: str):
    file_path = os.path.join("normalized_image", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")  

@router.get("/download_image_resized/{filename}")
async def download_image_resized(filename: str):
    file_path = os.path.join("resized_image", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")      