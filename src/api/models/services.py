from pydantic import BaseModel

class ItemIn(BaseModel):
    name: str | None = None
    subtitle: str | None = None
    logo: str | None = None
    icon: str | None = None
    url: str | None = None
    target: str | None = None
    order: int | None = None
    background: str | None = None
    tag: str | None = None
    # Custom Item Attributes
    type: str | None = None
    endpoint: str | None = None
    useCredentials: bool | None = None
    location: str | None = None
    locationId: str | None = None
    apikey: str | None = None
    units: str | None = None
    legacyApi: bool | None = None
    method: str | None = None
    environments: list[str] | None = None
    libraryType: str | None = None
    slug: str | None = None
    xmlrpc: str | None = None
    rateInterval: str | None = None
    torrentInterval: str | None = None
    username: str | None = None
    password: str | None = None
    node: str | None = None
    warning_value: str | None = None
    danger_value: str | None = None
    api_token: str | None = None
    hide_decimals: str | None = None
    hide: list[str] | None = None
    small_font_on_small_screens: bool | None = None
    small_font_on_desktop: bool | None = None
    clipboard: str | None = None
    downloadInterval: str | None = None
    display: str | None = None

class ItemOut(ItemIn):
    id: int | None = None

class ServiceIn(BaseModel):
    name: str | None = None
    order: int | None = None
    icon: str | None = None

class ServiceOut(ServiceIn):
    id: int | None = None
    items: list[ItemOut] | None = []
