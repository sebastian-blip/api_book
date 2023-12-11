from pydantic import BaseModel
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
