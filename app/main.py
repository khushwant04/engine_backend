from fastapi import FastAPI
from app.api.endpoints import boxes, image_services



app = FastAPI()



app.include_router(boxes.router, prefix="/api/boxes", tags=["Bounding Boxes"])
app.include_router(image_services.router, prefix="/api/image_services", tags=["Process Image"])