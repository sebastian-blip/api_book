import logging
import yaml

from functools import lru_cache
from pydantic import BaseSettings
from metadata.path import Path


class DevConfig:
    docs_url = '/docs'
    redoc_url = None
    URL_ALLLOWED_CORS = ['*']


class ProdConfig:
    docs_url = None
    redoc_url = None
    URL_ALLLOWED_CORS = ['*']


class TestConfig:
    docs_url = '/docs'
    redoc_url = None
    URL_ALLLOWED_CORS = ['*']


class Settings(BaseSettings):
    app_name: str = 'Api-books'


@lru_cache()
def get_config() -> dict:
    """Lectura del archivo de configuración"""

    with open(Path.config, encoding='utf8') as config_features:
        config = yaml.full_load(config_features)

    return config


@lru_cache()
def get_config_env():
    """Obtiene de la configuración del ambiente desplegado. El ambiente
    se indica en el config.yaml en la variable ENV.
    """
    config_env = {'PROD': ProdConfig, 'TEST': TestConfig, 'DEV': DevConfig}
    env = config_env[get_config().get('env')]

    return env


@lru_cache()
def get_log():
    """Creación del logger de la aplicación"""
    return logging.getLogger('uvicorn.info')
