from fastapi import APIRouter, HTTPException
from ..models.services import Service, ServiceIn, ServiceModify, Item, ItemIn
from ..helpers.id import get_max_id, get_max_order
from ..helpers.file import read_config, write_config

router = APIRouter(
    prefix="/config/service",
    tags=['Services']
)


@router.get(path='s', response_model=list[Service])
async def get_services():
    return read_config().services


@router.post('/', response_model=Service)
async def new_service(service: ServiceIn):
    config = read_config()

    if service.name in [x.name for x in config.services]:
        raise HTTPException(
            409, f'Service with name "{service.name}" already exists')

    service = Service(**service.dict())

    new_id = get_max_id(config.services) + 1
    service.id = new_id

    if service.order == None:
        service.order = get_max_order(config.services) + 1

    config.services.append(service)

    services = write_config(config).services
    service = list(filter(lambda x: x.id == new_id, services))[0]

    return service


@router.get(path='/{id}', response_model=Service)
async def get_service(id: int):
    services = read_config().services
    service = list(filter(lambda x: x.id == id, services))

    if len(service) == 1:
        return service[0]
    else:
        raise HTTPException(404, f'Service with id {id} not found')


@router.patch(path='/{id}', response_model=Service)
async def patch_service(id: int, service_modify: ServiceModify):
    config = read_config()

    original_service = list(filter(lambda x: x.id == id, config.services))
    if len(original_service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')
    original_service = original_service[0]

    remaining_services = list(filter(lambda x: x.id != id, config.services))

    service_modify = {
        k: v for (k, v) in service_modify.dict().items() if v != None}
    service_temp = original_service.dict()
    service_temp.update(service_modify)
    service_temp = Service(**service_temp)

    remaining_services.append(service_temp)
    config.services = remaining_services

    write_config(config)
    return service_temp


@router.delete(path='/{id}', response_model=Service)
async def delete_service(id: int):
    config = read_config()

    removed_service = list(filter(lambda x: x.id == id, config.services))

    if len(removed_service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')

    remaining_services = list(filter(lambda x: x.id != id, config.services))
    config.services = remaining_services
    write_config(config)

    return removed_service[0]


@router.post(path='/{service_id}/item', response_model=Item | None)
async def new_item(service_id: int, item: ItemIn):
    config = read_config()

    service = list(filter(lambda x: x.id == service_id, config.services))

    if len(service) != 1:
        raise HTTPException(404, f'Service with id {id} not found')

    service = service[0]

    if item.name in [x.name for x in service.items]:
        raise HTTPException(
            409, f'Item with name "{service.name}" already exists in Service {service.name}')

    item = Item(**item.dict())

    new_id = get_max_id(service.items) + 1
    item.id = new_id

    if item.order == None:
        item.order = get_max_order(service.items) + 1

    service.items.append(item)

    services = write_config(config).services

    service = list(filter(lambda x: x.id == service_id, services))[0]
    item = list(filter(lambda x: x.id == new_id, service.items))[0]

    return item


@router.get(path='/{service_id}/item/{item_id}', response_model=Item)
async def get_item(service_id: int, item_id: int):
    services = read_config().services
    service = list(filter(lambda x: x.id == service_id, services))

    if len(service) == 1:
        service = service[0]
    else:
        raise HTTPException(404, f'Service with id {service_id} not found')

    item = list(filter(lambda x: x.id == item_id, service.items))

    if len(item) == 1:
        return item[0]
    else:
        raise HTTPException(404, f'Item with id {item_id} not found')


@router.patch(path='/{service_id}/item/{item_id}', response_model=Item)
async def patch_item(service_id: int, item_id: int):
    pass


@router.delete(path='/{service_id}/item/{item_id}', response_model=Item)
async def delete_item(service_id: int, item_id: int):
    pass
