from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """Modelo que contiene los atributos del usuario"""

    username: str
    password: str
