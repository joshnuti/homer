from pydantic import BaseModel
from enum import Enum
from .link import Link

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

class Config(BaseModel):
    title: str
    subtitle: str | None = ''
    documentTitle: str | None = ''
    logo: str | None = ''
    icon: str | None = ''
    header: bool | None = True
    footer: bool | str | None = False
    columns: int | str | None = 'auto'
    connectivityCheck: bool | None = False
    defaults: Defaults | None = None
    theme: str | None = 'default'
    stylesheet: list[str] | None = []
    links: list[Link]

class ConfigIn(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    documentTitle: str | None = None
    logo: str | None = None
    icon: str | None = None
    header: bool | None = None
    footer: bool | str | None = None
    columns: int | str | None = None
    connectivityCheck: bool | None = None
    defaults: Defaults | None = None
    theme: str | None = None
    stylesheet: list[str] | None = None