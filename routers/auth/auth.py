from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from parser.user_parser import User
from utils.validate_user import validar_usuario
from utils.auth import create_access_token


auth_router = APIRouter(prefix='/auth', tags=['auth_router'])


@auth_router.post(path='/get-token', status_code=200)
async def get_token(user_data: User) -> JSONResponse:
    """

    Args:
        user_data: Datos del usuario

    Returns:
        token jwt si los datos son validos

    """

    usurio_valido = await validar_usuario(
        user_data.username, user_data.password
    )

    if not usurio_valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='credenciales no validas',
        )

    else:
        token = create_access_token(user_data.username)
        respuesta = JSONResponse(status_code=200, content={'jwt_token': token})

    return respuesta
