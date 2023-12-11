from config import get_bd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from parser.parser_books import AttributesBooks
from utils.buscar_book_api import buscar_google_api


books_router = APIRouter(prefix='/books', tags=['books_router'])


@books_router.post(path="/get-book", status_code=200)
async def get_book(atri_book: AttributesBooks) -> dict:
    """Endpoint que busca un libro en la bd interna o un API externa.

    Args:
        atri_book: Atributos para la búsqueda del libro.

    Returns:
        Resultado de la busqueda.

    """
    fuente = 'bd interna'
    mongo_bd = get_bd()
    book_collection = mongo_bd['books']

    atri_to_search = {
        atribute: value for atribute, value in dict(atri_book).items() if value
    }

    if not atri_to_search:
        raise HTTPException(
            status_code=422, detail='Se debe enviar por lo menos un parametro.'
        )

    else:
        projection = {'_id': False}
        description_book = await book_collection.find_one(
            atri_to_search, projection=projection
        )

        if not description_book:
            description_book = await buscar_google_api(atri_to_search)
            fuente = 'google'

        if not description_book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

    description_book['fuente'] = fuente

    return description_book
