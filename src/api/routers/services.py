from fastapi import APIRouter
from ..helpers.models import Service, ServiceIn
from ..helpers.config import read_config, write_config

router = APIRouter(
    prefix="/services",
    tags=['Services']
)

@router.get(path='/services', response_model=list[Service])
async def get_categories():
    return read_config()['services']


@router.post('/services/', response_model=list[Service])
async def new_service(service: ServiceIn):
    config = read_config()

    print(service.dict())
    
    config['services'].append(service.dict())

    return write_config(config)