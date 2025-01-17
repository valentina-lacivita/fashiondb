from enum import Enum

import numpy as np
from pydantic import computed_field
from sqlmodel import SQLModel, Column, JSON, Field

class FormatDownscaleFactor(int, Enum):
    original = 1 # 28x28
    medium = 2   # 14x14
    small = 4    # 07x07

class Image(SQLModel, table=True):
    id: str = Field(primary_key=True)
    label: int 
    format_downscale_factor: FormatDownscaleFactor=FormatDownscaleFactor.original
    data: list[int] = Field(sa_column=Column(JSON))

    def as_sq_array(self):
        image_array = np.array(self.data)
        dim = int(np.sqrt(image_array.shape[0]))
        try:
            return image_array.reshape((dim, dim))
        except ValueError:
            raise ValueError("Data cannot be reshaped into a square matrix")

    @computed_field
    @property
    def as_array(self) -> list[list[int]]:
        image_array = self.as_sq_array()        
        if self.format_downscale_factor > 1:
            image_array = image_array[::self.format_downscale_factor, ::self.format_downscale_factor]
        return image_array.tolist()
