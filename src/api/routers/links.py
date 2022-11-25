from fastapi import APIRouter
from ..helpers.models import Link
from ..helpers.config import read_config, write_config

router = APIRouter(
    prefix="/link",
    tags=['Links']
)

@router.get('s', response_model=list[Link], tags=['Links'])
async def get_links():
    return read_config()['links']

@router.post('', response_model=Link, tags=['Links'])
async def new_link(link: Link):
    config = read_config()
    config['links'].append(link.dict())
    
    links = write_config(config)['links']
    filtered_links = list(filter(lambda x: x['name'] == link.name, links))

    if len(filtered_links) == 1:
        return filtered_links[0]
    else:
        return None

@router.get('/{name}', response_model=Link, tags=['Links'])
async def get_link(name: str):
    links = read_config()['links']
    filtered_links = list(filter(lambda x: x['name'] == name, links))

    if len(filtered_links) == 1:
        return filtered_links[0]
    else:
        return None
    
@router.patch('/{name}', response_model=Link, tags=['Links'])
async def patch_link(name: str, link: Link):
    pass

@router.delete('/{name}', response_model=Link, tags=['Links'])
async def delete_link(name: str):
    config = read_config()
    removed_links = list(filter(lambda x: x['name'] == name, config['links']))
    filtered_links = list(filter(lambda x: x['name'] != name, config['links']))

    config['links'] = filtered_links

    write_config(config)

    if len(removed_links) == 1:
        return removed_links[0]
    else:
        return None