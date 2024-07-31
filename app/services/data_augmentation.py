from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import aiofiles
import io
import os
import numpy as np
from fastapi import UploadFile


# Directory to save processed images
PROCESSED_IMAGES_DIR = "outputs/augemented_images"

if not os.path.exists(PROCESSED_IMAGES_DIR):
    os.makedirs(PROCESSED_IMAGES_DIR)

async def save_image(image: Image.Image, file: UploadFile, prefix: str) -> str:
    output_filename = f"{prefix}_{file.filename}"
    output_path = os.path.join("output", output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    async with aiofiles.open(output_path, 'wb') as out_file:
        image.save(out_file, format=image.format)
    return output_filename

async def augment_images(files: list[UploadFile], rotate: int = 0, flip_horizontal: bool = False, flip_vertical: bool = False,
                        brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0, hue: float = 0.0,
                        noise_level: float = 0.0, blur_radius: float = 0.0) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))

            if rotate:
                image = image.rotate(rotate)
            if flip_horizontal:
                image = ImageOps.mirror(image)
            if flip_vertical:
                image = ImageOps.flip(image)
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(brightness)
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(contrast)
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(saturation)
            if hue != 0.0:
                image = image.convert('HSV')
                np_img = np.array(image)
                np_img[..., 0] = (np_img[..., 0].astype(int) + int(hue * 255)) % 255
                image = Image.fromarray(np_img, 'HSV').convert('RGB')
            if noise_level > 0.0:
                np_img = np.array(image)
                noise = np.random.normal(0, noise_level, np_img.shape).astype(np.uint8)
                np_img = np.clip(np_img + noise, 0, 255)
                image = Image.fromarray(np_img)
            if blur_radius > 0.0:
                image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            output_filename = await save_image(image, file, "augmented")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

# Functions for individual augmentations with level control

async def rotate_images(files: list[UploadFile], rotate: int) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image = image.rotate(rotate)
            output_filename = await save_image(image, file, "rotated")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def flip_images(files: list[UploadFile], flip_horizontal: bool, flip_vertical: bool) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            if flip_horizontal:
                image = ImageOps.mirror(image)
            if flip_vertical:
                image = ImageOps.flip(image)
            output_filename = await save_image(image, file, "flipped")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def adjust_brightness(files: list[UploadFile], brightness: float) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)
            output_filename = await save_image(image, file, "brightness_adjusted")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def adjust_contrast(files: list[UploadFile], contrast: float) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)
            output_filename = await save_image(image, file, "contrast_adjusted")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def adjust_saturation(files: list[UploadFile], saturation: float) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(saturation)
            output_filename = await save_image(image, file, "saturation_adjusted")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def adjust_hue(files: list[UploadFile], hue: float) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image = image.convert('HSV')
            np_img = np.array(image)
            np_img[..., 0] = (np_img[..., 0].astype(int) + int(hue * 255)) % 255
            image = Image.fromarray(np_img, 'HSV').convert('RGB')
            output_filename = await save_image(image, file, "hue_adjusted")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def add_gaussian_noise(files: list[UploadFile], noise_level: float) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            if noise_level > 0.0:
                np_img = np.array(image)
                noise = np.random.normal(0, noise_level, np_img.shape).astype(np.uint8)
                np_img = np.clip(np_img + noise, 0, 255)
                image = Image.fromarray(np_img)
            output_filename = await save_image(image, file, "gaussian_noise_added")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e

async def apply_blur(files: list[UploadFile], blur_radius: float) -> list[str]:
    output_filenames = []
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            if blur_radius > 0.0:
                image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            output_filename = await save_image(image, file, "blur_applied")
            output_filenames.append(output_filename)
        
        return output_filenames
    except Exception as e:
        raise e
