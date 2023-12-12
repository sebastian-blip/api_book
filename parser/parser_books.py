from pydantic import BaseModel, field_validator
from fastapi import HTTPException
from typing import Optional


class AttributesBooks(BaseModel):
    """Modelo que contiene los atributos por los cuales puede ser buscado un libro"""

    id: Optional[str] = None
    titulo: Optional[str] = None
    subtitulo: Optional[str] = None
    autor: Optional[str] = None
    catergorias: Optional[str] = None
    fecha_publicacion: Optional[str] = None
    editor: Optional[str] = None
    descripcion: Optional[str] = None


class CrearBook(BaseModel):
    id: str
    fuente: str

    @field_validator('fuente')
    def validar_fuente(cls, fuente: str) -> str:
        """

        Args:
            fuente: Fuente donde se debe buscar el libro sea google o open.

        Returns:
            La fuente si esta es válida, de lo contraria retornará un error 442

        """
        tipo_fuentes = ['google', 'open']
        if fuente not in tipo_fuentes:
            msg = f'Las fuentes validas son: {tipo_fuentes}'
            raise HTTPException(status_code=422, detail=msg)

        return fuente
