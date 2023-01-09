from fastapi import APIRouter, HTTPException, Header
from ..models.services import ItemIn, ItemOut
from ..helpers.file import read_config_http, write_config_http
from ..helpers.listofmodels import ListOfModels
from .services import get_service_helper

router = APIRouter(
    prefix="/config/service",
    tags=['Service Items'],
)


def get_item_helper(items: list[ItemOut], id: int) -> ItemOut:
    item = list(filter(lambda x: x.id == id, items))

    if len(item) == 0:
        raise HTTPException(404, f'Item with id {id} not found')
    elif len(item) > 1:
        raise HTTPException(409, f'Too many items found with id {id}')

    return item[0]


@router.post(path='/{service_id}/item', response_model=ItemOut | None, status_code=201, response_model_exclude_none=True)
async def new_item(service_id: int, item: ItemIn, CONFIG_PATH: str | None = Header(None)):
    if item.name == None:
        raise HTTPException(
            400, 'name is a required field')

    config = read_config_http(CONFIG_PATH)

    service = list(filter(lambda x: x.id == service_id, config.services))

    if len(service) != 1:
        raise HTTPException(404, f'Service with id {id} not found')

    service = service[0]
    service.items = ListOfModels(service.items)

    if item.name in [x.name for x in service.items]:
        raise HTTPException(
            409, f'Item with name "{service.name}" already exists in Service {service.name}')

    item = ItemOut(**item.dict())

    new_id = service.items.max_id() + 1
    item.id = new_id

    if item.order == None:
        item.order = service.items.max_order() + 1

    service.items.append(item)

    services = write_config_http(CONFIG_PATH, config).services

    service = list(filter(lambda x: x.id == service_id, services))[0]
    item = list(filter(lambda x: x.id == new_id, service.items))[0]

    return item


@router.get(path='/{service_id}/item/{item_id}', response_model=ItemOut, response_model_exclude_none=True)
async def get_item(service_id: int, item_id: int, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    service = get_service_helper(config.services, service_id)
    return get_item_helper(service.items, item_id)


@router.patch(path='/{service_id}/item/{item_id}', response_model=ItemOut, status_code=200, response_model_exclude_none=True)
async def patch_item(service_id: int, item_id: int, item_modify: ItemIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    service = get_service_helper(config.services, service_id)

    original_item = get_item_helper(service.items, item_id)

    remaining_items = list(filter(lambda x: x.id != item_id, service.items))

    item_modify = {
        k: v for (k, v) in item_modify.dict().items() if v != None}
    item_temp = original_item.dict()
    item_temp.update(item_modify)
    item_temp = ItemOut(**item_temp)

    remaining_items.append(item_temp)
    service.items = remaining_items

    write_config_http(CONFIG_PATH, config)
    return item_temp


@router.put(path='/{service_id}/item/{item_id}', response_model=ItemOut, status_code=200, response_model_exclude_none=True)
async def put_item(service_id: int, item_id: int, item_modify: ItemIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    service = get_service_helper(config.services, service_id)

    original_item = get_item_helper(service.items, item_id)

    remaining_items = list(filter(lambda x: x.id != item_id, service.items))

    new_item = ItemOut(**item_modify.dict())
    new_item.id = original_item.id
    remaining_items.append(new_item)
    service.items = remaining_items

    write_config_http(CONFIG_PATH, config)
    return new_item


@router.delete(path='/{service_id}/item/{item_id}', response_model=ItemOut, response_model_exclude_none=True)
async def delete_item(service_id: int, item_id: int, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)
    service = get_service_helper(config.services, service_id)

    removed_item = get_item_helper(service.items, item_id)

    remaining_items = list(filter(lambda x: x.id != item_id, service.items))
    service.items = remaining_items

    write_config_http(CONFIG_PATH, config)

    return removed_item
