import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings, get_config_env


app = FastAPI(
    title='Api-books',
    version='0.1.0',
    docs_url=get_config_env().docs_url,
    redoc_url=get_config_env().redoc_url,
)

origins = get_config_env().URL_ALLLOWED_CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run(app)
