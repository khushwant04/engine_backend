from fastapi import FastAPI
from app.api.endpoints import boxes, image_process



app = FastAPI()



app.include_router(boxes.router, prefix="/api/boxes", tags=["Bounding Boxes"])
app.include_router(image_process.router, prefix="/api/image-process", tags=["Image Processing"])