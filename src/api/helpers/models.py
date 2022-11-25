from pydantic import BaseModel
from enum import Enum

class Layout(Enum):
    columns = 'columns'
    list = 'list'

class ColorTheme(Enum):
    light = 'light'
    dark = 'dark'
    auto = 'auto'

class Defaults(BaseModel):
    layout: Layout
    colorTheme: ColorTheme
    
class Link(BaseModel):
    name: str
    url: str
    icon: str | None = ''
    target: str | None = ''

class Item(BaseModel):
    name: str
    logo: str | None = ''
    icon: str | None = ''
    subtitle: str | None = ''
    url: str | None = ''
    type: str | None = ''
    target: str | None = ''
    background: str | None = ''

class Service(BaseModel):
    name: str
    icon: str | None = ''
    items: list[Item]

class ServiceIn(BaseModel):
    name: str
    icon: str | None = ''
    items: list[Item] | None = []