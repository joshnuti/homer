from __future__ import annotations

def get_max_id(models: list[Item] | list[Service] | list[Link]):
    if len(models) == 0:
        return 0
    
    return max(models, key=lambda x: x.id).id

def get_max_order(models: list[Item] | list[Service] | list[Link]):
    if len(models) == 0:
        return 0
    
    return max(models, key=lambda x: x.order).order