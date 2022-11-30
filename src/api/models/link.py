from pydantic import BaseModel

class Link(BaseModel):
    id: int | None = -1
    order: int | None = -1
    name: str
    url: str
    icon: str | None = ''
    target: str | None = ''