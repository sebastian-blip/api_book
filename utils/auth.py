import jwt
from datetime import datetime, timedelta


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