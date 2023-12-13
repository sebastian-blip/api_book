import os
import httpx

from metadata.google import GoogleBookApi
from metadata.openlibrary import OpenLibraryApi


async def buscar_google_api(client: httpx, atributos: dict) -> dict | None:
    """Función para hacer búsquedas de libros con el api de google

    Args:
        atributos: Atributos que se utilizaran para la búsqueda del libro
        client: instancia de httpx para hacer request asincronico

    Returns:
        Datos del libro, en caso que no se encuentre el libro retorna un None

    """
    primer_atributo = list(atributos.values())[0]
    atributos_search = {'q': primer_atributo}

    for key, value in atributos.items():
        atributo = GoogleBookApi.google_atributos.get(key)

        if atributo:
            atributos_search[atributo] = value

    api_google_key = os.getenv('GOOGLE_API_KEY')
    atributos_search['key'] = api_google_key
    response = await client.get(GoogleBookApi.url, params=atributos_search)

    if response.status_code == 200 and 'items' in response.json():
        data_book = response.json()["items"][0]
        info_book = data_book['volumeInfo']
        info_book['id'] = data_book['id']
        info_book = {
            value: info_book.get(clave, None)
            for clave, value in GoogleBookApi.rename_atributos.items()
        }

        info_book['autor'] = ','.join(info_book['autor'])
        info_book['categorias'] = ','.join(info_book['categorias'])
        info_book['subtitulo'] = None
        info_book['fuente'] = 'google'

        return info_book

    return {}


async def buscar_open_api(client: httpx, atributos: dict) -> dict | None:
    """Función para hacer búsquedas de libros con el api de Open Library

    Args:
        atributos: Atributos que se utilizaran para la búsqueda del libro
        client: instancia de httpx para hacer request asincronico

    Returns:
        Datos del libro, en caso que no se encuentre el libro retorna un None

    """
    atributos_search = {'sort': 'new'}

    for key, value in atributos.items():
        atributo = OpenLibraryApi.open_atributos.get(key)

        if atributo:
            atributos_search[atributo] = value

    response = await client.get(url=OpenLibraryApi.url, params=atributos_search)
    if response.status_code == 200 and response.json()['docs']:
        info_book = response.json()["docs"][0]
        info_book['key'] = info_book['key'].split('/')[2]
        info_book = {
            value: info_book.get(clave, None)
            for clave, value in OpenLibraryApi.rename_atributos.items()
        }

        info_book['autor'] = ','.join(info_book['autor'])
        info_book['editor'] = ','.join(info_book['editor'])
        info_book['fecha_publicacion'] = ','.join(
            info_book['fecha_publicacion']
        )
        info_book['subtitulo'] = None
        info_book['fuente'] = 'open'
        if info_book['categorias']:
            info_book['descripcion'] = info_book['categorias'][0]

        return info_book

    return {}
