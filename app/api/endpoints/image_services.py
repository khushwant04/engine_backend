from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from app.services.image_services import resize_images, normalize_image
from typing import List
import os 




router = APIRouter()



@router.post("/resize/")
async def resize_images_endpoint(width: int, height: int, files: List[UploadFile] = File(...)):
    """
    Resizes a list of uploaded images to a specified width and height.

    Parameters:
        width (int): The desired width of the resized image.
        height (int): The desired height of the resized image.
        files (List[UploadFile], optional): A list of uploaded image files.

    Returns:
        dict: A dictionary containing the message "Images resized successfully" and the resized images.

    Raises:
        HTTPException: If an error occurs during the resizing process.

    """
    try:
        size = (width, height)
        resized_images = await resize_images(size, files)
        return {"message": "Images resized successfully", "data": resized_images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/normalize-image/")
async def normalize_image_endpoint(files: List[UploadFile] = File(...)):
    """
    Endpoint for normalizing a list of uploaded image files.

    Parameters:
        files (List[UploadFile]): A list of uploaded image files.

    Returns:
        JSONResponse: A JSON response containing the normalized image.

    Raises:
        HTTPException: If an HTTP exception occurs during the normalization process.
        Exception: If any other exception occurs during the normalization process.
    """
    try:
        normalized_image = await normalize_image(files)
        return JSONResponse(content={"normalized_image": normalized_image})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  
  
  
  
    
@router.get("/download_image_normalized/{filename}")
async def download_normalized_image(filename: str) -> FileResponse:
    """
    Downloads a normalized image file from the server.

    Args:
        filename (str): The name of the image file to download.

    Returns:
        FileResponse: The normalized image file as a response.

    Raises:
        HTTPException: If the specified file does not exist.
    """
    normalized_image_path = os.path.join("normalized_image", filename)
    if os.path.exists(normalized_image_path):
        return FileResponse(normalized_image_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")




@router.get("/download_image_resized/{image_filename}")
async def download_resized_image(
    image_filename: str
) -> FileResponse:
    """
    Downloads a resized image file from the server.

    Args:
        image_filename (str): The name of the image file to download.

    Returns:
        FileResponse: The resized image file as a response.

    Raises:
        HTTPException: If the specified file does not exist.
    """
    resized_image_path = os.path.join("resized_image", image_filename)
    if os.path.exists(resized_image_path):
        return FileResponse(resized_image_path, filename=image_filename)
    raise HTTPException(status_code=404, detail="File not found")
