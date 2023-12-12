import httpx
import traceback
import asyncio
from config import get_bd
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse


from config import get_log
from parser.parser_books import AttributesBooks, CrearBook
from utils.auth import verificar_token
from utils.buscar_book_api import buscar_google_api, buscar_open_api


books_router = APIRouter(prefix='/books', tags=['books_router'])


@books_router.post(
    path="/get-book", status_code=200, dependencies=[Depends(verificar_token)]
)
async def get_book(atri_book: AttributesBooks) -> JSONResponse:
    """Endpoint que busca un libro en la bd interna o un API externa.

    Args:
        atri_book: Atributos para la búsqueda del libro.

    Returns:
        Resultado de la busqueda.

    """
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
            async with httpx.AsyncClient() as client:
                google_task = buscar_google_api(client, atri_to_search)
                open_task = buscar_open_api(client, atri_to_search)
                description_book = await asyncio.gather(google_task, open_task)
                description_book = max(
                    description_book,
                    key=lambda x: len([v for v in x.values() if v is not None]),
                )

        else:
            description_book['fuente'] = 'bd interna'

        if not description_book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

    result = JSONResponse(status_code=200, content=description_book)

    return result


@books_router.post(path='/create-book', dependencies=[Depends(verificar_token)])
async def create_book(book_data: CrearBook) -> JSONResponse:
    """

    Args:
        id: Id del libro
        fuente: Fuente donde se encuentran los datos del libro.

    Returns:
        Crea el registro en la bd interna y si este es creado correctamente
        retorna un 201

    """

    funciones_busqueda = {'google': buscar_google_api, 'open': buscar_open_api}

    mongo_bd = get_bd()
    book_collection = mongo_bd['books']
    projection = {'_id': False}
    atri_to_search = {'id': book_data.id}
    description_book = await book_collection.find_one(
        atri_to_search, projection=projection
    )

    if description_book:
        raise HTTPException(
            status_code=409, detail='El libro ya existe en la base de datos'
        )

    try:
        async with httpx.AsyncClient() as client:
            description_book = await funciones_busqueda.get(book_data.fuente)(
                client, atri_to_search
            )
        await book_collection.insert_one(description_book)
        detail = (
            f'El libro {description_book["titulo"]} se guardo correctamente'
        )
        return JSONResponse(status_code=202, content=detail)

    except Exception as e:
        log = get_log()
        log.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail='No se pudo crear el libro')


@books_router.delete(
    path='/delete-book',
    status_code=200,
    dependencies=[Depends(verificar_token)],
)
async def delete_book(id: str) -> JSONResponse:
    """

    Args:
        id: Id del libro que se quiere borrar de la bd

    """

    mongo_bd = get_bd()
    book_collection = mongo_bd['books']

    atri_to_delete = {'id': id}
    description_book = await book_collection.delete_one(atri_to_delete)

    if description_book.deleted_count > 0:
        result = JSONResponse(
            status_code=200, content='Libro borrado correctamente'
        )
    else:
        result = JSONResponse(
            status_code=404, content='Libro no encontrado en la bd'
        )

    return result
