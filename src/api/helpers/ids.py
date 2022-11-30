from __future__ import annotations

def assign_missing_ids(models: list[Item] | list[Service] | list[Link]):
    max_id = max(models, key = lambda x: x.id).id
    if max_id == -1:
        max_id = 1

    for elem in list(filter(lambda x : x.id == -1, models)): 
        elem.id == max_id
        max_id += 1