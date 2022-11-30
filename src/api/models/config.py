from pydantic import BaseModel
from enum import Enum
from .link import Link
from .services import Service
from .colors import Colors

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

class MessageMapping(BaseModel):
    title: str | None = None
    content: str | None = None

class Message(BaseModel):
    url: str | None = None
    mapping: MessageMapping | None = None
    style: str | None = None
    title: str | None = None
    icon: str | None = None
    content: str | None = None

class Config(BaseModel):
    externalConfig: str | None = None
    ###
    title: str | None = None
    subtitle: str | None = None
    documentTitle: str | None= None
    ###
    logo: str | None = None
    icon: str | None = None
    ##
    header: bool | None = None
    footer: bool | str | None = None
    ##
    columns: int | str | None = None
    connectivityCheck: bool | None = None
    ##
    defaults: Defaults | None = None
    ##
    theme: str | None = None
    ##
    stylesheet: list[str] | None = None
    ##
    colors: Colors | None = None
    ## 
    # message: Message | None = None
    links: list[Link] | None = None
    services: list[Service] | None = None

class ConfigIn(BaseModel):
    externalConfig: str | None = None
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
    message: Message | None = None