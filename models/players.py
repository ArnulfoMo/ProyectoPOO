from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
import re

class Player(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el jugador."
    )

    firstname: Optional[str] = Field(
        description="Primer nombre del jugador",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["Juan","Maria"]
    )

    lastname: Optional[str] = Field(
        description="Apellido del jugador",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["Perez","Martinez"]
    )

    nickname: Optional[str] = Field(
        description="Apodo único del jugador.",
        pattern=r"^[A-Za-z0-9_]+$",
        default=None,
        examples=["juampi", "mary_gz"]
    )

    email: Optional[str] = Field(
        description="Email del jugador",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        default=None,
        examples=["usuario@example.com"]
    )

    birth_date: Optional[date] = Field(
        description="Fecha de nacimiento del jugador.",
        default=None,
        examples=["1999-05-12", "2000-10-25"]
    )
