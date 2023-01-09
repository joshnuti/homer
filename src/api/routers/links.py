from fastapi import APIRouter, HTTPException, Header
from ..models.link import LinkIn, LinkOut
from ..helpers.file import read_config_http, write_config_http
from ..helpers.listofmodels import ListOfModels

router = APIRouter(
    prefix="/config/link",
    tags=['Links']
)


@router.get('', name='Get All Links', response_model=list[LinkOut], response_model_exclude_none=True)
async def get_links(CONFIG_PATH: str | None = Header(None)):
    return read_config_http(CONFIG_PATH).links


@router.post('', response_model=LinkOut, status_code=201, response_model_exclude_none=True)
async def new_link(link: LinkIn, CONFIG_PATH: str | None = Header(None)):
    if link.name == None:
        raise HTTPException(
            400, 'name is a required field')

    if link.url == None:
        raise HTTPException(
            400, 'url is a required field')

    config = read_config_http(CONFIG_PATH)

    if link.name in [x.name for x in config.links]:
        raise HTTPException(
            409, f'Link with name "{link.name}" already exists')

    link = LinkOut(**link.dict())

    config.links = ListOfModels(config.links)
    new_id = config.links.max_id() + 1
    link.id = new_id
    if link.order == None: link.order = config.links.max_order() + 1

    config.links.append(link)

    links = write_config_http(CONFIG_PATH, config).links
    link = list(filter(lambda x: x.id == new_id, links))[0]

    return link


@router.get('/{id}', response_model=LinkOut | None, response_model_exclude_none=True)
async def get_link(id: int, CONFIG_PATH: str | None = Header(None)):
    links = read_config_http(CONFIG_PATH).links
    link = list(filter(lambda x: x.id == id, links))

    if len(link) == 1: return link[0]
    else: raise HTTPException(404, f'Link with id {id} not found')


@router.patch('/{id}', response_model=LinkOut, status_code=200, response_model_exclude_none=True)
async def patch_link(id: int, link_modify: LinkIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    original_link = list(filter(lambda x: x.id == id, config.links))
    if len(original_link) == 0: raise HTTPException(
        404, f'Link with id {id} not found')
    original_link = original_link[0]

    remaining_links = list(filter(lambda x: x.id != id, config.links))

    link_modify = {k: v for (k, v) in link_modify.dict().items() if v != None}
    link_temp = original_link.dict()
    link_temp.update(link_modify)
    link_temp = LinkOut(**link_temp)

    remaining_links.append(link_temp)
    config.links = remaining_links

    write_config_http(CONFIG_PATH, config)
    return link_temp


@router.put('/{id}', response_model=LinkOut, status_code=200, response_model_exclude_none=True)
async def put_link(id: int, link_modify: LinkIn, CONFIG_PATH: str | None = Header(None)):
    config = read_config_http(CONFIG_PATH)

    original_link = list(filter(lambda x: x.id == id, config.links))
    if len(original_link) == 0: raise HTTPException(
        404, f'Link with id {id} not found')
    original_link = original_link[0]

    remaining_links = list(filter(lambda x: x.id != id, config.links))

    new_link = LinkOut(**link_modify.dict())
    new_link.id = original_link.id
    remaining_links.append(new_link)
    config.links = remaining_links

    write_config_http(CONFIG_PATH, config)
    return new_link

@ router.delete('/{id}', response_model=LinkOut, response_model_exclude_none=True)
async def delete_link(id: int, CONFIG_PATH: str | None=Header(None)):
    config = read_config_http(CONFIG_PATH)

    removed_link = list(filter(lambda x: x.id == id, config.links))

    if len(removed_link) == 0: raise HTTPException(
        404, f'Link with id {id} not found')
    remaining_links = list(filter(lambda x: x.id != id, config.links))

    config.links = remaining_links

    write_config_http(CONFIG_PATH, config)

    return removed_link[0]
