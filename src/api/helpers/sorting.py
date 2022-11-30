from __future__ import annotations

def sort_model(models: list[Item] | list[Service] | list[Link]):
    return sorted(models, lambda x: (x.order, x.name))