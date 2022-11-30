from fastapi import APIRouter
from ..models.config import Config, ConfigIn
from ..helpers.file import read_config, write_config

router = APIRouter(
    prefix="/config",
    tags=['Config']
)

@router.get('', response_model=Config)
async def get_config():
    config = read_config()
    return config

@router.patch('', response_model=Config)
async def patch_config(new_config: ConfigIn):
    config = read_config()
    new_config = { k:v for (k,v) in new_config.dict().items() if v != None}

    if new_config['defaults']['layout']: 
        new_config['defaults']['layout'] = new_config['defaults']['layout'].value

    if new_config['defaults']['colorTheme']: 
        new_config['defaults']['colorTheme'] = new_config['defaults']['colorTheme'].value

    config.update(new_config)

    return write_config(config)