from fastapi import FastAPI
from app.api.endpoints import (
    augment, boxes, image_process
)


app = FastAPI()



app.include_router(boxes.router, prefix="/api/v1/boxes", tags=["Bounding Boxes"])
app.include_router(image_process.router, prefix="/api/v1/image-process", tags=["Image Processing"])
app.include_router(augment.router, prefix="/api/v1/augment", tags=["Augmentation"])