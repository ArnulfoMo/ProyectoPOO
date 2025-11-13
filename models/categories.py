from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
import re

class Player(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID autoincrementable de la categoría."
    )

    name: Optional[str] = Field(
        description="Nombre de la categoría del juego.",
        pattern=r"^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9][A-Za-zÁÉÍÓÚÑáéíóúñ0-9 ':-]*$",
        default=None,
        examples=["Action", "Adventure", "Role-Playing", "Sports"]
    )

    description: Optional[str] = Field(
        description="Descripción detallada de la categoría.",
        pattern=r"^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9.,;:!¿?¡()\"'/%\- ]+$",
        default=None,
        examples=[
            "Fast-paced games focused on combat and movement.",
            "Story-driven games centered on exploration and character development."
        ]
    )