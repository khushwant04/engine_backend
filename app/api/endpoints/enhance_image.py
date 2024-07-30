from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from urllib.parse import unquote
from fastapi.responses import FileResponse, JSONResponse
from app.services.real_esrgan import enhance_images
from typing import List



# Define the API router

router = APIRouter()


@router.post("/enhance/")
async def enhance_images_endpoint(files: List[UploadFile] = File(...)):
    """
    Endpoint for enhancing images.

    Args:
        files (List[UploadFile]): A list of uploaded image files.

    Returns:
        JSONResponse: A JSON response containing a message indicating that the images were enhanced successfully and the output filenames.

    Raises:
        None.
    """
    input_folder = "temp_inputs"
    output_folder = "results"
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    input_paths = []
    for file in files:
        input_path = os.path.join(input_folder, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        input_paths.append(input_path)

    enhance_images(input_paths=input_paths, output_folder=output_folder)

    output_files = [file.filename for file in files]

    # Clean up input folder
    shutil.rmtree(input_folder)

    return JSONResponse(content={"message": "Images enhanced successfully", "output_files": output_files})

@router.get("/download_image/{filename}")
async def download_image(filename: str):
    """
    Endpoint for downloading an enhanced image.

    Args:
        filename (str): The name of the file to download.

    Returns:
        FileResponse: A response with the file to download.

    Raises:
        HTTPException: If the file does not exist.
    """
    file_path = os.path.join("results", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")