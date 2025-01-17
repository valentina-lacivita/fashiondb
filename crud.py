from model import Image, FormatDownscaleFactor
from sqlmodel import Session, select

def get_images(session: Session, label: int) -> list[Image]:
    images = session.exec(select(Image).where(Image.label == label)).all()
    return images

def get_image(session: Session, image_id: str) -> Image:
    image = session.exec(select(Image).where(Image.id == image_id)).first()
    if image is None:
        raise ValueError(f"Image with id {image_id} not found.")
    return image

def update_image_format(session: Session, image_id: str, format_downscale_factor: FormatDownscaleFactor) -> Image:
    if format_downscale_factor not in FormatDownscaleFactor:
        raise ValueError(f"Invalid downscale factor: {format_downscale_factor}.")
    image = session.exec(select(Image).where(Image.id == image_id)).first()
    if image is None:
        raise ValueError(f"Image with id {image_id} not found.")
    image.format_downscale_factor = format_downscale_factor
    session.commit()
    session.refresh(image)
    return image

def insert_image(session: Session, image: Image) -> Image:
    session.add(image)
    session.commit()
    session.refresh(image)
    return image

def delete_image(session: Session, image_id: str) -> Image:
    image = session.exec(select(Image).where(Image.id == image_id)).first()
    if image is None:
        raise ValueError(f"Image with id {image_id} not found.")
    session.delete(image)
    session.commit()
    return image
