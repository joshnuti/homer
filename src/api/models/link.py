from pydantic import BaseModel

class LinkIn(BaseModel):
    order: int | None = None
    name: str | None = None
    url: str | None = None
    icon: str | None = None
    target: str | None = None

class LinkOut(LinkIn):
    id: int | None = None