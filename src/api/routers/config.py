from fastapi import APIRouter
from ..models.config import Config, ConfigIn
from ..helpers.file import read_config, write_config

router = APIRouter(
    prefix="/config",
    tags=['Config']
)

@router.get('', response_model=Config)
async def get_config():
    return read_config()

@router.patch('', response_model=Config)
async def patch_config(new_config: ConfigIn):
    config = read_config()

    new_config = { k:v for (k,v) in new_config.dict().items() if v != None}

    config = config.dict()
    config.update(new_config)
    config = Config(**config)

    return write_config(config)