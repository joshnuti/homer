from fastapi import APIRouter, Header
from ..models.config import Config, ConfigIn
from ..helpers.file import write_config_http, read_config_http

router = APIRouter(
    prefix="/config",
    tags=['Config'], 
)

@router.get('', response_model=Config)
async def get_config(CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    return config

@router.patch('', response_model=Config)
async def patch_config(new_config: ConfigIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    new_config = { k:v for (k,v) in new_config.dict().items() if v != None}

    config = config.dict()
    config.update(new_config)
    config = Config(**config)

    return write_config_http(CONFIG_PATH, config)