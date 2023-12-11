from config import get_bd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import traceback

from config import get_log
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


@books_router.post(path='/create-book')
async def create_book(id: str, fuente: str):
    """

    Args:
        id: Id del libro
        fuente: Fuente donde se encuentran los datos del libro.

    Returns:
        Crea el registro en la bd interna y si este es creado correctamente
        retorna un 201

    """

    funciones_busqueda = {'google': buscar_google_api}

    mongo_bd = get_bd()
    book_collection = mongo_bd['books']
    projection = {'_id': False}
    atri_to_search = {'id': id}
    description_book = await book_collection.find_one(
        atri_to_search, projection=projection
    )

    if description_book:
        raise HTTPException(
            status_code=409, detail='El libro ya se existe en la base de datos'
        )

    try:
        description_book = await funciones_busqueda.get(fuente)(atri_to_search)
        await book_collection.insert_one(description_book)
        detail = (
            f'El libro {description_book["titulo"]} se guardo correctamente'
        )
        return JSONResponse(status_code=202, content=detail)

    except Exception as e:
        log = get_log()
        log.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail='No se pudo crear el libro')
