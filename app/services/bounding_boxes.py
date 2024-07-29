import os
import pandas as pd
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from fastapi import UploadFile
from io import BytesIO
from typing import List
from zipfile import ZipFile, BadZipFile


# Device and dtype setup
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32


# Model and Processor initialization
model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large-ft", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large-ft", trust_remote_code=True)

# Define the prompt
prompt = "<OD>"


def save_bounding_boxes_to_excel(data, excel_filename):
    """
    Saves the given data to an Excel file.

    Args:
        data (list[dict]): A list of dictionaries containing the data to be saved.
        excel_filename (str): The name of the Excel file to be created.

    Returns:
        None

    This function takes a list of dictionaries containing data and saves it to an Excel file.
    The data is converted into a pandas DataFrame and then saved to the specified Excel file.
    The index is not included in the Excel file.
    """
    df = pd.DataFrame(data)
    df.to_excel(excel_filename, index=False)


async def process_images(files: List[UploadFile]):
        """
        Asynchronously processes a list of uploaded image files and generates bounding box data.

        Args:
            files (List[UploadFile]): A list of uploaded image files.

        Returns:
            List[Dict[str, Union[str, int, float]]]: A list of dictionaries containing image name, class name, X, Y, Width, and Height values for each bounding box.

        This function iterates over each uploaded image file and performs the following steps:
        1. Opens the image using the PIL library.
        2. Retrieves the image name from the file.
        3. Preprocesses the image using the `processor` object and generates text using the `model` object.
        4. Parses the generated text using the `processor` object to extract bounding box and label information.
        5. Zips the bounding box and label information together and appends it to the `data` list.
        6. Returns the `data` list.

        Note: This function assumes that the necessary dependencies, such as the `Image` and `BytesIO` modules from the PIL library, the `AutoProcessor` and `AutoModelForCausalLM` classes from the `transformers` library, and the `torch` library, are imported at the top of the file.
        """
        data = []

        for file in files:
            image = Image.open(BytesIO(await file.read()))
            image_name = file.filename

            inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)
            generated_ids = model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=1024,
                do_sample=False,
                num_beams=3
            )
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
            parsed_answer = processor.post_process_generation(generated_text, task="<OD>", image_size=(image.width, image.height))

            bboxes = parsed_answer['<OD>']['bboxes']
            labels = parsed_answer['<OD>']['labels']

            for bbox, label in zip(bboxes, labels):
                x, y, width, height = bbox
                data.append({
                    "Image Name": image_name,
                    "Class Name": label,
                    "X": x,
                    "Y": y,
                    "Width": width,
                    "Height": height
                })

        return  data 


async def generate_excel(files: List[UploadFile], excel_filename: str):
    """
    Generate an Excel file containing bounding boxes data from a list of uploaded images.

    Args:
        files (List[UploadFile]): A list of uploaded image files.
        excel_filename (str): The name of the Excel file to be generated.

    Returns:
        str: The name of the generated Excel file.

    This function takes a list of uploaded image files and processes them using the `process_images` function.
    The resulting bounding boxes data is then saved to an Excel file using the `save_bounding_boxes_to_excel` function.
    The name of the generated Excel file is returned.
    """
    data = await process_images(files)
    save_bounding_boxes_to_excel(data, excel_filename)
    return excel_filename

