from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Platform(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID autoincrementable de la plataforma."
    )

    name: Optional[str] = Field(
        default=None,
        description="Nombre de la plataforma.",
        pattern=r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ' \-]+$",
        examples=["PlayStation 5", "Nintendo Switch", "Xbox Series X"]
    )

    release_date: Optional[date] = Field(
        default=None,
        description="Fecha de lanzamiento de la plataforma.",
        examples=["2020-11-12", "2017-03-03"]
    )
