from fastapi import APIRouter
from ..models.services import Service, ServiceIn
from ..helpers.file import read_config, write_config

router = APIRouter(
    prefix="/config/services",
    tags=['Services']
)

@router.get(path='/', response_model=list[Service])
async def get_categories():
    return read_config()['services']


@router.post('/', response_model=list[Service])
async def new_service(service: ServiceIn):
    config = read_config()

    return write_config(config)