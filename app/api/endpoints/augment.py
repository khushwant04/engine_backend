from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from app.services.data_augmentation import (
    augment_images,
    rotate_images,
    flip_images,
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    adjust_hue,
    add_gaussian_noise,
    apply_blur
)
import os
import zipfile
from io import BytesIO

router = APIRouter()

@router.post("/default_augment/")
async def augment_images_endpoint(
    files: list[UploadFile] = File(...),
    rotate: int = Form(0),
    flip_horizontal: bool = Form(False),
    flip_vertical: bool = Form(False),
    brightness: float = Form(1.0),
    contrast: float = Form(1.0),
    saturation: float = Form(1.0),
    hue: float = Form(0.0),
    gaussian_noise: bool = Form(False),
    noise_level: float = Form(25.0),
    blur: bool = Form(False),
    blur_radius: float = Form(2.0)
):
    try:
        result = await augment_images(
            files, rotate, flip_horizontal, flip_vertical,
            brightness, contrast, saturation, hue,
            gaussian_noise, noise_level, blur, blur_radius
        )
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/rotate/")
async def rotate_images_endpoint(files: list[UploadFile] = File(...), rotate: int = Form(...)):
    try:
        result = await rotate_images(files, rotate)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/flip/")
async def flip_images_endpoint(
    files: list[UploadFile] = File(...),
    flip_horizontal: bool = Form(False),
    flip_vertical: bool = Form(False)
):
    try:
        result = await flip_images(files, flip_horizontal, flip_vertical)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/brightness/")
async def adjust_brightness_endpoint(files: list[UploadFile] = File(...), brightness: float = Form(...)):
    try:
        result = await adjust_brightness(files, brightness)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/contrast/")
async def adjust_contrast_endpoint(files: list[UploadFile] = File(...), contrast: float = Form(...)):
    try:
        result = await adjust_contrast(files, contrast)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/saturation/")
async def adjust_saturation_endpoint(files: list[UploadFile] = File(...), saturation: float = Form(...)):
    try:
        result = await adjust_saturation(files, saturation)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/hue/")
async def adjust_hue_endpoint(files: list[UploadFile] = File(...), hue: float = Form(...)):
    try:
        result = await adjust_hue(files, hue)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gaussian_noise/")
async def add_gaussian_noise_endpoint(
    files: list[UploadFile] = File(...),
    gaussian_noise: bool = Form(...),
    noise_level: float = Form(25.0)
):
    try:
        result = await add_gaussian_noise(files, gaussian_noise, noise_level)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/blur/")
async def apply_blur_endpoint(
    files: list[UploadFile] = File(...),
    blur: bool = Form(False),
    blur_radius: float = Form(2.0)
):
    try:
        result = await apply_blur(files, blur, blur_radius)
        return JSONResponse(content={"filenames": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download/")
async def download_augmented_images():
    try:
        output_dir = "/outputs/augmented_images"
        if not os.path.exists(output_dir) or not os.listdir(output_dir):
            raise HTTPException(status_code=404, detail="No images found to download")

        # Create a BytesIO object to hold the zip file in memory
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, output_dir))

        zip_buffer.seek(0)  # Move to the beginning of the BytesIO object

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=augmented_images.zip"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    
