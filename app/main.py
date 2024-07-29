from fastapi import FastAPI
from app.api.endpoints import boxes, enhance_image



app = FastAPI()



app.include_router(boxes.router, prefix="/api/boxes", tags=["Bounding Boxes"])
app.include_router(enhance_image.router, prefix="/api/enhance", tags=["Enhance Image"])
