from fastapi import APIRouter, HTTPException, Header
from ..models.services import Service, ServiceIn, ServiceModify, Item, ItemIn, ItemModify
from ..helpers.file import read_config_http, write_config_http

router = APIRouter(
    prefix="/config/service",
    tags=['Services'],
)

# region helpers

def get_service_helper(services: list[Service], id: int) -> Service:
    service = list(filter(lambda x: x.id == id, services))

    if len(service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')
    elif len(service) > 1:
        raise HTTPException(409, f'Too many services found with id {id}')
        
    return service[0]

def get_item_helper(items: list[Item], id: int) -> Item:
    item = list(filter(lambda x: x.id == id, items))

    if len(item) == 0:
        raise HTTPException(404, f'Item with id {id} not found')
    elif len(item) > 1:
        raise HTTPException(409, f'Too many items found with id {id}')

    return item[0]

# endregion


@router.get(path='s', response_model=list[Service])
async def get_services(CONFIG_PATH: str | None = Header(None)):
    return read_config_http(CONFIG_PATH).services


@router.post('/', response_model=Service)
async def new_service(service: ServiceIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    if service.name in [x.name for x in config.services]:
        raise HTTPException(
            409, f'Service with name "{service.name}" already exists')

    service = Service(**service.dict())

    new_id = config.services.max_id() + 1
    service.id = new_id

    if service.order == None:
        service.order = config.services.max_order() + 1

    config.services.append(service)

    services = write_config_http(CONFIG_PATH, config).services
    service = list(filter(lambda x: x.id == new_id, services))[0]

    return service


@router.get(path='/{id}', response_model=Service)
async def get_service(id: int, CONFIG_PATH: str | None = Header(None)):
    return get_service_helper(read_config_http(CONFIG_PATH), id)


@router.patch(path='/{id}', response_model=Service)
async def patch_service(id: int, service_modify: ServiceModify, CONFIG_PATH: str | None = Header(None)):
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
    service_temp = Service(**service_temp)

    remaining_services.append(service_temp)
    config.services = remaining_services

    write_config_http(CONFIG_PATH, config)
    return service_temp


@router.delete(path='/{id}', response_model=Service)
async def delete_service(id: int, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    removed_service = list(filter(lambda x: x.id == id, config.services))

    if len(removed_service) == 0:
        raise HTTPException(404, f'Service with id {id} not found')

    remaining_services = list(filter(lambda x: x.id != id, config.services))
    config.services = remaining_services
    write_config_http(CONFIG_PATH, config)

    return removed_service[0]


@router.post(path='/{service_id}/item', response_model=Item | None)
async def new_item(service_id: int, item: ItemIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    service = list(filter(lambda x: x.id == service_id, config.services))

    if len(service) != 1:
        raise HTTPException(404, f'Service with id {id} not found')

    service = service[0]

    if item.name in [x.name for x in service.items]:
        raise HTTPException(
            409, f'Item with name "{service.name}" already exists in Service {service.name}')

    item = Item(**item.dict())

    new_id = service.items.max_id() + 1
    item.id = new_id

    if item.order == None:
        item.order = service.items.max_order() + 1

    service.items.append(item)

    services = write_config_http(CONFIG_PATH, config).services

    service = list(filter(lambda x: x.id == service_id, services))[0]
    item = list(filter(lambda x: x.id == new_id, service.items))[0]

    return item


@router.get(path='/{service_id}/item/{item_id}', response_model=Item)
async def get_item(service_id: int, item_id: int, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    service = get_service_helper(config.services, service_id)
    return get_item_helper(service.items, item_id)

@router.patch(path='/{service_id}/item/{item_id}', response_model=Item)
async def patch_item(service_id: int, item_id: int, item_modify: ItemModify, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    service = get_service_helper(config.services, service_id)
    
    original_item = get_item_helper(service.items, item_id)

    remaining_items = list(filter(lambda x: x.id != item_id, service.items))

    item_modify = {
        k: v for (k, v) in item_modify.dict().items() if v != None}
    item_temp = original_item.dict()
    item_temp.update(item_modify)
    item_temp = Item(**item_temp)

    remaining_items.append(item_temp)
    service.items = remaining_items

    write_config_http(CONFIG_PATH, config)
    return item_temp


@router.delete(path='/{service_id}/item/{item_id}', response_model=Item)
async def delete_item(service_id: int, item_id: int, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    service = get_service_helper(config.services, service_id)

    removed_item = get_item_helper(service.items, {item_id})

    remaining_items = list(filter(lambda x: x.id != item_id, service.items))
    service.items = remaining_items

    write_config_http(CONFIG_PATH, config)

    return removed_item
        