from pydantic import BaseModel

class Link(BaseModel):
    id: int | None = None
    order: int | None = None
    name: str
    url: str
    icon: str | None = None
    target: str | None = None

class LinkIn(BaseModel):
    order: int | None = None
    name: str
    url: str
    icon: str | None = None
    target: str | None = None

class LinkModify(BaseModel):
    order: int | None = None
    name: str | None = None
    url: str | None = None
    icon: str | None = None
    target: str | None = None