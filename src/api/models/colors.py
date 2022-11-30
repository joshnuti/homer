from pydantic import BaseModel

class ColorsDetail(BaseModel):
    highlight_primary: str | None = None
    highlight_secondary: str | None = None
    highlight_hover: str | None = None
    background: str | None = None
    card_background: str | None = None
    text: str | None = None
    text_header: str | None = None
    text_title: str | None = None
    text_subtitle: str | None = None
    card_shadow: str
    link: str | None = None
    link_hover: str | None = None
    background_image: str | None = None
    
class Colors(BaseModel):
    dark: ColorsDetail
    light: ColorsDetail

# config['colors']['dark'] = { k.replace('-', '_'):v for (k,v) in config['colors']['dark'].items() }
# config['colors']['light'] = { k.replace('-', '_'):v for (k,v) in config['colors']['light'].items() }

# config['colors']['dark']['card_shadow'] = Color(config['colors']['dark']['card_shadow']).as_rgb()
# config['colors']['light']['card_shadow'] = Color(config['colors']['light']['card_shadow']).as_rgb()