import cv2
import numpy as np
import os
from typing import List
from fastapi import UploadFile
from uuid import uuid4

# Directory to save processed images
PROCESSED_IMAGES_DIR = "outputs/processed_images"

if not os.path.exists(PROCESSED_IMAGES_DIR):
    os.makedirs(PROCESSED_IMAGES_DIR)

def save_image(image: np.ndarray, prefix: str) -> str:
    filename = f"{prefix}_{uuid4().hex}.png"
    filepath = os.path.join(PROCESSED_IMAGES_DIR, filename)
    cv2.imwrite(filepath, image)
    return filepath

async def resize_images(images: List[UploadFile], width: int, height: int) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            resized_img = cv2.resize(img, (width, height))
            filepath = save_image(resized_img, "resized")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to resize image {image.filename}: {e}")
    return filepaths

async def normalize_images(images: List[UploadFile]) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            normalized_img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
            filepath = save_image(normalized_img, "normalized")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to normalize image {image.filename}: {e}")
    return filepaths

async def crop_images(images: List[UploadFile], x: int, y: int, width: int, height: int) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            cropped_img = img[y:y+height, x:x+width]
            filepath = save_image(cropped_img, "cropped")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to crop image {image.filename}: {e}")
    return filepaths

async def rotate_flip_images(images: List[UploadFile], rotate_angle: int = 0, flip_code: int = 1) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            if rotate_angle:
                (h, w) = img.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
                img = cv2.warpAffine(img, M, (w, h))
            if flip_code is not None:
                img = cv2.flip(img, flip_code)
            filepath = save_image(img, "rotated_flipped")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to process image {image.filename}: {e}")
    return filepaths

async def adjust_color_images(images: List[UploadFile], brightness: int = 0, contrast: int = 0, saturation: int = 0) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            img = cv2.convertScaleAbs(img, alpha=1 + contrast / 127.0, beta=brightness)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv[..., 1] = cv2.add(hsv[..., 1], saturation)
            img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            filepath = save_image(img, "color_adjusted")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to adjust color of image {image.filename}: {e}")
    return filepaths

async def reduce_noise_images(images: List[UploadFile]) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            noise_reduced_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            filepath = save_image(noise_reduced_img, "noise_reduced")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to reduce noise in image {image.filename}: {e}")
    return filepaths

async def remove_background_images(images: List[UploadFile]) -> List[str]:
    filepaths = []
    for image in images:
        try:
            contents = await image.read()
            np_img = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            mask = np.zeros(img.shape[:2], np.uint8)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            rect = (50, 50, img.shape[1] - 50, img.shape[0] - 50)
            cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img = img * mask2[:, :, np.newaxis]
            filepath = save_image(img, "background_removed")
            filepaths.append(filepath)
        except Exception as e:
            print(f"Failed to remove background from image {image.filename}: {e}")
    return filepaths
