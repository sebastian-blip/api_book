import httpx
import pytest
from utils.buscar_book_api import buscar_google_api, buscar_open_api


@pytest.mark.asyncio
async def test_buscar_google_api():
    """ Test de la función que busca un libro en google api

    """

    async with httpx.AsyncClient() as client:
        atributos = {'titulo': 'Harry Potter'}
        resultado = await buscar_google_api(client, atributos)
        assert resultado is not None


@pytest.mark.asyncio
async def test_buscar_open_api():
    """ Test de la función que busca un libro en open api

    """

    async with httpx.AsyncClient() as client:
        atributos = {'titulo': 'Harry Potter'}
        resultado = await buscar_open_api(client, atributos)
        assert resultado is not None

