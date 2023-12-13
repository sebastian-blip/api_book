import jwt

from datetime import datetime, timedelta
from fastapi import HTTPException, status, Header
from typing import Annotated


from config import get_llaves_jwt


def create_access_token(user: str) -> jwt:
    """Crea un token de inicio de sección para el usuario válido.

    Args:
        user: usuario válido al que pertenece el token.
        hours: tiempo en horas de validez del token.

     Returns:
         token asociado al usuario.

    """

    keys = get_llaves_jwt()
    secret_key = keys['private_jwt_key']
    data = {
        'user_id': None,
        'username': user,
        'exp': datetime.utcnow() + timedelta(hours=3),
    }

    return jwt.encode(data, secret_key, algorithm='RS512')


def decode_token(token: str) -> dict:
    """Función para decodificar el token de sesión.

    Args:
        token: Token a decodificar.

    Returns:
        datos del usuario al que pertenece el token

        .. code-block:: python

           {"user_id": None, "username": user}

    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='No se pueden validar las credenciales',
    )
    keys = get_llaves_jwt()
    secret_key = keys['public_jwt_key']
    try:
        data_user = jwt.decode(token, secret_key, algorithms=['RS512'])
        success = True
        message = ''
    except Exception as e:
        success = False
        message = credentials_exception
        data_user = None

    return dict(data=data_user, success=success, msg=message)


async def verificar_token(token: Annotated[str, Header()]):
    """Verifica si el token es válido y permite el paso a
    los endpoint.

    Args:
        token: Token correspondiente a la información del usuario.

    Returns:
        retorna la información del usuario si fue validada
        correctamente.

    """

    data_user = decode_token(token)
    if data_user['success']:
        username = data_user['data'].get('username')
    else:
        raise data_user['msg']

    return username
