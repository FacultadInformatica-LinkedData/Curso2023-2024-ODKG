import logging
from copy import deepcopy
from functools import lru_cache
from typing import Union, Any

from pydantic import BaseSettings
from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG


class Settings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 5000
    WORKERS: int = 1
    LOG_LEVEL: Union[int, str] = logging.INFO
    LOGGING_CONFIG: dict[str, Any] = deepcopy({
        **UVICORN_LOGGING_CONFIG,
        **{
            'formatters': {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(asctime)s %(levelprefix)s %(message)s",
                    "use_colors": None,
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                },
            }
        }
    })
    DEBUG: bool = False
    AUTH: str = ''

    class Config:
        env_file = "../.env"


@lru_cache()
def get_config():
    return Settings()


current_config = get_config()

for k, v in list(current_config):
    globals()[k] = v
