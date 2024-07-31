"""
This module contains the endpoints for the bounding boxes API.

This API allows users to generate bounding boxes for uploaded images and download the generated bounding boxes data in an Excel file.

Endpoints:
    - POST /api/boxes/generate: Generates bounding boxes for a list of uploaded images.
    - GET /api/boxes/download: Downloads the bounding boxes data in an Excel file.

Imports:
    - fastapi: Provides the necessary classes and functions for building the API.
    - UploadFile: Allows the API to accept file uploads.
    - File: Allows the API to accept file uploads.
    - HTTPException: Allows the API to handle exceptions.
    - FileResponse: Allows the API to return a file as a response.
    - process_images: A function from the app.services.bounding_boxes module that processes the uploaded images and generates bounding boxes.
    - generate_excel: A function from the app.services.bounding_boxes module that generates an Excel file containing the bounding boxes data.
"""


from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.bounding_boxes import process_images, generate_excel
from typing import List


# Define the API router
router = APIRouter()


@router.post("/generate")
async def generate_boxes(files: List[UploadFile] = File(...)):
    """
    Generate bounding boxes for a list of uploaded images.

    Parameters:
        files (List[UploadFile]): A list of uploaded image files.

    Returns:
        dict: A dictionary containing a message indicating that the bounding boxes are generated and the filename of the generated Excel file.
    """
    data = await process_images(files)
    return {"message": "Bounding boxes are generated.", "excel_filename": data}



@router.post("/generate_excel")
async def generate_boxes(files: List[UploadFile] = File(...)):
    """
    Generate bounding boxes for a list of uploaded images and save them to an Excel file.

    Parameters:
        files (List[UploadFile]): A list of uploaded image files.

    Returns:
        dict: A dictionary containing a message indicating that the bounding boxes are generated and the filename of the generated Excel file.

    Raises:
        HTTPException: If an error occurs during the generation or saving of the bounding boxes.

    """
    excel_filename = "bounding_boxes.xlsx"
    try:
        await generate_excel(files, excel_filename)
        return {"message": "Bounding boxes generated and saved to Excel.", "excel_filename": excel_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/download")
async def download_boxes():
    """
    Downloads the bounding boxes data from the 'bounding_boxes.xlsx' file.

    Returns:
        FileResponse: A response object containing the file to download.

    Raises:
        None.
    """
    excel_filename = "bounding_boxes.xlsx"
    return FileResponse(path=excel_filename, filename=excel_filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

