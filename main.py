import os

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session

from db import get_session
from crud import get_images, get_image, update_image_format, insert_image, delete_image
from model import Image, FormatDownscaleFactor

app = FastAPI(title="FashionDB")

@app.post("/images", response_model=Image)
async def insert_img(image: Image, session: Session=Depends(get_session)) -> Image:
    try:
        image = insert_image(session, image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return image

@app.get("/images", response_model=list[Image])
async def get_imgs(label: int, session: Session=Depends(get_session)) -> list[Image]:
    images = get_images(session, label)
    return images

@app.get("/images/{image_id}", response_model=Image)
async def get_img(image_id: str, session: Session=Depends(get_session)) -> Image:
    image = get_image(session, image_id)
    if not image:
        raise HTTPException(status_code=404, detail=f"Image {image_id} not found.")
    return image

@app.patch("/images/{image_id}", response_model=Image)
async def update_image(image_id: str, image_format: FormatDownscaleFactor, session: Session=Depends(get_session)) -> Image:
    updated_image = update_image_format(session, image_id, image_format)
    if not updated_image:
        raise HTTPException(status_code=404, detail=f"Image {image_id} not found.")
    return updated_image

@app.delete("/images/{image_id}")
async def delete_img(image_id: str, session: Session=Depends(get_session)) -> JSONResponse:
    image = delete_image(session, image_id)
    if not image:
        raise HTTPException(status_code=404, detail=f"Image {image_id} not found.")
    return JSONResponse(content={"message": f"Image {image_id} was deleted successfully."})


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app="main:app", host=host, port=port, reload=True)
