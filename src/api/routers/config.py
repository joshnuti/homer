from fastapi import APIRouter, Header, HTTPException
from ..models.config import Config, ConfigIn
from ..helpers.file import write_config_http, read_config_http, copy_defaults
from ..helpers.exceptions import ConfigFileNotFound

router = APIRouter(
    prefix="/config",
    tags=['Config'], 
)

@router.get('', response_model=Config, response_model_exclude_none=True)
async def get_config(CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    return config

@router.patch('', response_model=Config, status_code=201, response_model_exclude_none=True)
async def patch_config(new_config: ConfigIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    new_config = { k:v for (k,v) in new_config.dict().items() if v != None}

    config = config.dict()
    config.update(new_config)
    config = Config(**config)

    return write_config_http(CONFIG_PATH, config)

@router.put('/defaults', response_model=Config, status_code=201, response_model_exclude_none=True)
async def put_default_config(CONFIG_PATH: str | None = Header(None)):
    try:
        copy_defaults(CONFIG_PATH)
    except ConfigFileNotFound:
        raise HTTPException(500, 'Unable to copy defaults')

    return read_config_http(CONFIG_PATH)