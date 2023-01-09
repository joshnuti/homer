from fastapi import APIRouter, HTTPException, Header
from ..models.services import ServiceOut, ServiceIn
from ..helpers.file import read_config_http, write_config_http
from ..helpers.listofmodels import ListOfModels

router = APIRouter(
    prefix="/config/service",
    tags=['Services'],
)


def get_service_helper(services: list[ServiceOut], id: int) -> ServiceOut:
    service = list(filter(lambda x: x.id == id, services))

    if len(service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')
    elif len(service) > 1:
        raise HTTPException(409, f'Too many services found with id {id}')

    return service[0]


@router.get(path='s', response_model=list[ServiceOut], response_model_exclude_none=True)
async def get_services(CONFIG_PATH: str | None = Header(None)):
    return read_config_http(CONFIG_PATH).services


@router.post('', response_model=ServiceOut, status_code=201, response_model_exclude_none=True)
async def new_service(service: ServiceIn, CONFIG_PATH: str | None = Header(None)):
    if service.name == None:
        raise HTTPException(
            400, 'name is a required field')

    config = read_config_http(CONFIG_PATH)

    if service.name in [x.name for x in config.services]:
        raise HTTPException(
            409, f'Service with name "{service.name}" already exists')

    service = ServiceOut(**service.dict())

    config.services = ListOfModels(config.services)
    new_id = config.services.max_id() + 1
    service.id = new_id

    if service.order == None:
        service.order = config.services.max_order() + 1

    config.services.append(service)

    services = write_config_http(CONFIG_PATH, config).services
    service = list(filter(lambda x: x.id == new_id, services))[0]

    return service


@router.get(path='/{id}', response_model=ServiceOut, response_model_exclude_none=True)
async def get_service(id: int, CONFIG_PATH: str | None = Header(None)):
    return get_service_helper(read_config_http(CONFIG_PATH).services, id)


@router.patch(path='/{id}', response_model=ServiceOut, status_code=200, response_model_exclude_none=True)
async def patch_service(id: int, service_modify: ServiceIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    original_service = list(filter(lambda x: x.id == id, config.services))
    if len(original_service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')
    original_service = original_service[0]

    remaining_services = list(filter(lambda x: x.id != id, config.services))

    service_modify = {
        k: v for (k, v) in service_modify.dict().items() if v != None}
    service_temp = original_service.dict()
    service_temp.update(service_modify)
    service_temp = ServiceOut(**service_temp)

    remaining_services.append(service_temp)
    config.services = remaining_services

    write_config_http(CONFIG_PATH, config)
    return service_temp


@router.put(path='/{id}', response_model=ServiceOut, status_code=200, response_model_exclude_none=True)
async def put_service(id: int, service_modify: ServiceIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    original_service = list(filter(lambda x: x.id == id, config.services))
    if len(original_service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')
    original_service = original_service[0]

    remaining_services = list(filter(lambda x: x.id != id, config.services))

    new_service = ServiceOut(**service_modify.dict())
    new_service.id = original_service.id
    remaining_services.append(new_service)
    config.services = remaining_services

    write_config_http(CONFIG_PATH, config)
    return new_service


@router.delete(path='/{id}', response_model=ServiceOut, response_model_exclude_none=True)
async def delete_service(id: int, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    removed_service = list(filter(lambda x: x.id == id, config.services))

    if len(removed_service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')

    remaining_services = list(filter(lambda x: x.id != id, config.services))
    config.services = remaining_services
    write_config_http(CONFIG_PATH, config)

    return removed_service[0]
