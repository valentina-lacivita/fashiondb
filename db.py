from pathlib import Path

import numpy as np
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

from model import Image, FormatDownscaleFactor

# DB
engine = create_engine(
    "sqlite:///database.db", 
    echo=True, 
    connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

## SEED DATA
DATA_PATH = Path("./data")
IMAGES_FILE = DATA_PATH / "sample_images.npy"
LABELS_FILE = DATA_PATH / "sample_labels.npy"
IDS_FILE = DATA_PATH / "sample_ids.npy"

def load_sample_images(
        ids_file: str | Path=IDS_FILE,
        labels_file: str | Path=LABELS_FILE, 
        images_file: str | Path=IMAGES_FILE, 
    ) -> list[Image]:
    images = np.load(images_file, allow_pickle=False)
    labels = np.load(labels_file, allow_pickle=False)
    ids = np.load(ids_file, allow_pickle=False)
    
    return [
        dict(id=img_id, label=int(labels[i]), format_downscale_factor=FormatDownscaleFactor.original, data=images[i].tolist())
        for i, img_id in enumerate(ids)
    ]

with Session(engine) as session:
    stmt = sqlite_upsert(Image).values(load_sample_images())
    stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
    session.execute(stmt)
    session.commit()


