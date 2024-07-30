import os
import cv2
from PIL import Image
from fastapi import UploadFile
from typing import List
from io import BytesIO
from fastapi import HTTPException
import numpy as  np

async def resize_images(size: tuple, images: List[UploadFile]):
    data = []

    try:
        for image in images:
            # Read the image with PIL
            pil_image = Image.open(BytesIO(await image.read()))
            # Convert PIL image to OpenCV format
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            # Resize the image with OpenCV
            resized_image = cv2.resize(cv_image, size)
            # Save or process the resized image as needed
            output_path = f"resized_image/{image.filename}"
            cv2.imwrite(output_path, resized_image)
            data.append(output_path)
            
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def normalize_image(images: List[UploadFile]) -> List[str]:
    data = []
    try:
        for image in images:
            # Read image from UploadFile
            file_bytes = np.frombuffer(await image.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            # Normalize the image
            norm_image = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

            # Ensure the output directory exists
            os.makedirs("resized_image", exist_ok=True)

            # Save the normalized image
            output_path = f"normalized_image/{image.filename}"
            cv2.imwrite(output_path, norm_image)
            data.append(output_path)
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))