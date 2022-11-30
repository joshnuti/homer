from fastapi import APIRouter, HTTPException
from ..models.link import Link, LinkIn, LinkModify
from ..helpers.file import read_config, write_config
from ..helpers.id import get_max_id, get_max_order

router = APIRouter(
    prefix="/config/link",
    tags=['Links']
)

@router.get('s', response_model=list[Link])
async def get_links():
    return read_config().links

@router.post('', response_model=Link)
async def new_link(link: LinkIn):
    config = read_config()

    if link.name in [x.name for x in config.links]:
        raise HTTPException(409, f'Link with name "{link.name}" already exists')

    link = Link(**link.dict())
    
    new_id = get_max_id(config.links) + 1
    link.id = new_id
    if link.order == None: link.order = get_max_order(config.links) + 1

    config.links.append(link)
    
    links = write_config(config).links
    link = list(filter(lambda x: x.id == new_id, links))[0]

    return link 

@router.get('/{id}', response_model=Link | None)
async def get_link(id: int):
    links = read_config().links
    link = list(filter(lambda x: x.id == id, links))

    if len(link) == 1: return link[0]
    else: raise HTTPException(404, f'Link with id {id} not found')
    
@router.patch('/{id}', response_model=Link)
async def patch_link(id: int, link_modify: LinkModify):
    config = read_config()

    original_link = list(filter(lambda x: x.id == id, config.links))
    if len(original_link) == 0: raise HTTPException(404, f'Link with id {id} not found')
    original_link = original_link[0]

    remaining_links = list(filter(lambda x: x.id != id, config.links))

    link_modify = { k:v for (k,v) in link_modify.dict().items() if v != None }
    link_temp = original_link.dict()
    link_temp.update(link_modify)
    link_temp = Link(**link_temp)

    remaining_links.append(link_temp)
    config.links = remaining_links

    write_config(config)
    return link_temp

@router.delete('/{id}', response_model=Link)
async def delete_link(id: int):
    config = read_config()

    removed_link = list(filter(lambda x: x.id == id, config.links))

    if len(removed_link) == 0: raise HTTPException(404, f'Link with id {id} not found')
    remaining_links = list(filter(lambda x: x.id != id, config.links))

    config.links = remaining_links

    write_config(config)

    return removed_link[0]