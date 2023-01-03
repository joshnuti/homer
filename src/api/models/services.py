from pydantic import BaseModel

class Item(BaseModel):
    id: int | None = None
    order: int | None = None
    name: str
    logo: str | None = None
    icon: str | None = None
    subtitle: str | None = None
    url: str | None = None
    type: str | None = None
    target: str | None = None
    background: str | None = None

class Service(BaseModel):
    id: int | None = None
    order: int | None = None
    name: str
    icon: str | None = None
    items: list[Item] | None = []

class ItemIn(BaseModel):
    order: int | None = None
    name: str
    logo: str | None = None
    icon: str | None = None
    subtitle: str | None = None
    url: str | None = None
    type: str | None = None
    target: str | None = None
    background: str | None = None
    
class ServiceIn(BaseModel):
    name: str
    order: int | None = None
    icon: str | None = None

class ServiceModify(BaseModel):
    name: str | None = None
    order: int | None = None
    icon: str | None = None
    # items: list[ItemIn] | None = []

class ItemModify(BaseModel):
    order: int | None = None
    name: str | None = None
    logo: str | None = None
    icon: str | None = None
    subtitle: str | None = None
    url: str | None = None
    type: str | None = None
    target: str | None = None
    background: str | None = None