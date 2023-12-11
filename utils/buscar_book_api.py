import requests

from metadata.google import GoogleBookApi


async def buscar_google_api(atributos: dict) -> dict | None:
    """Función para hacer búsquedas de libros con el api de google

    Args:
        atributos: Atributos que se utilizaran para la búsqueda del libro

    Returns:
        Datos del libro, en caso que no se encuentre el libro retorna un None

    """
    primer_atributo = list(atributos.values())[0]
    primer_atributo = primer_atributo.replace(' ', '%20')
    atributos_search = {'q': primer_atributo}

    for key, value in atributos.items():
        value = value.replace(' ', '%20')
        atributo = GoogleBookApi.google_atributos.get(key)

        if atributo:
            atributos_search[atributo] = value

    string_atributos = '+'.join(
        [
            f'{clave}:{valor}' if clave != 'q' else f'{clave}={valor}'
            for clave, valor in atributos_search.items()
        ]
    )
    google_api_url = f'{GoogleBookApi.url}{string_atributos}'
    google_api_url = f'{google_api_url}&{GoogleBookApi.key}'
    response = requests.get(google_api_url)

    if response.status_code == 200 and 'items' in response.json():
        data_book = response.json()["items"][0]
        info_book = data_book['volumeInfo']
        info_book['id'] = data_book['id']
        info_book = {
            GoogleBookApi.rename_atributos[clave]: info_book[clave]
            for clave in GoogleBookApi.atributos_book & info_book.keys()
        }

        return info_book

    return None
