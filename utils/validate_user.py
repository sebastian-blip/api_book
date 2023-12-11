import hashlib
import secrets

from config import get_bd


async def validar_usuario(usuario: str, password: str) -> bool:
    """Función para validar si el usuario si se encuentra en la bd y su
    contraseña es correcta.

    Args:
        usuario: Usuario a validar.
        password: Contraseña del usuario.

    Returns:
        Usuario.

    """

    respuesta = False

    mongo_bd = get_bd()
    book_collection = mongo_bd['users']

    projection = {'_id': False}
    user_data = await book_collection.find_one(
        {'username': usuario}, projection=projection
    )

    if user_data:
        passw = user_data['password']
        passw_db = hash_password(password)

        if secrets.compare_digest(passw_db, passw):
            respuesta = True

    return respuesta


def hash_password(password: str) -> hashlib:
    """Función que cifra la contraseña en un hash determinado.

    Args:
        password: Contraseña a cifrar.

    Returns:
        Password cifrada.

    """
    h = hashlib.sha256()
    h.update(password.encode('utf-8'))

    return h.hexdigest()
