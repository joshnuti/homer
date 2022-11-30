from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    logo: str | None = ''
    icon: str | None = ''
    subtitle: str | None = ''
    url: str | None = ''
    type: str | None = ''
    target: str | None = ''
    background: str | None = ''

class Service(BaseModel):
    id: int
    name: str
    icon: str | None = ''
    items: list[Item]

class ServiceIn(BaseModel):
    name: str
    icon: str | None = ''
    items: list[Item] | None = []