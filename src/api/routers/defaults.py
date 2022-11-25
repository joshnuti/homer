from fastapi import APIRouter
from ..helpers.models import Defaults
from ..helpers.config import read_config, write_config

router = APIRouter(
    prefix="/defaults",
    tags=['Defaults']
)

@router.get('', response_model=Defaults)
async def get_defaults():
    return read_config()['defaults']

@router.patch('', response_model=Defaults)
async def patch_defaults(defaults: Defaults):
    defaults = defaults.dict()
    defaults['layout'] = defaults['layout'].value
    defaults['colorTheme'] = defaults['colorTheme'].value

    config = read_config()
    config['defaults'] = defaults
    
    updated_config = write_config(config)

    return updated_config['defaults']