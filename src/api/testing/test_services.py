from .test_main import client

service_in = {
    "order": 5,
    "name": "Test Service 1",
    "icon": "fas fa-google",
}

service_out = {
    "id": 2,
    "order": 5,
    "name": "Test Service 1",
    "icon": "fas fa-google",
    "items": []
}

item_in = {
    "order": 5,
    "name": "Test Item 1",
    "icon": "fas fa-google",
    "subtitle": "subtitle",
    "url": "https://www.google.com",
}

item_out = {
    "id": 1,
    "order": 5,
    "name": "Test Item 1",
    "logo": None,
    "icon": "fas fa-google",
    "subtitle": "subtitle",
    "url": "https://www.google.com",
    "type": None,
    "target": None,
    "background": None
}


def test_reset_config():
    response = client.put('/config/defaults')
    assert response.status_code == 201

# region Services


def test_get():
    response = client.get("/config/services")
    assert response.status_code == 200


def test_get_invalid():
    response = client.get('/config/services', {})
    assert response.status_code == 403


def test_post():
    response = client.post('/config/service', service_in)
    assert response.status_code == 201
    assert response.json() == service_out


def test_post_conflict():
    response = client.post('/config/service', service_in)
    assert response.status_code == 409


def test_get_specific():
    response = client.get('/config/service/2')
    assert response.status_code == 200
    assert response.json() == service_out


def test_patch():
    response = client.patch('/config/service/2', {'name': 'Test Service 2'})
    assert response.status_code == 201
    service_out['name'] = 'Test Service 2'
    assert response.json() == service_out


def test_patch_notfound():
    response = client.patch('/config/service/3', {'name': 'Test Service 2'})
    assert response.status_code == 404

# endregion

# region Items


def test_item_post():
    response = client.post('/config/service/2/item', item_in)
    assert response.status_code == 201
    assert response.json() == item_out
    service_out["items"].append(item_out)


def test_item_post_conflict():
    response = client.post('/config/service/2/item', item_in)
    assert response.status_code == 409


def test_get_withitem():
    response = client.get('/config/service/2')
    assert response.status_code == 200
    assert response.json() == service_out


def test_item_get():
    response = client.get('/config/service/2/item/1')
    assert response.status_code == 200
    assert response.json() == item_out


def test_item_get_notfound1():
    response = client.get('/config/service/2/item/2')
    assert response.status_code == 404


def test_item_get_notfound2():
    response = client.get('/config/service/3/item/2')
    assert response.status_code == 404


def test_item_patch():
    response = client.patch('/config/service/2/item/1',
                            {'name': 'Test Item 2'})
    assert response.status_code == 201
    item_out['name'] = 'Test Item 2'
    assert response.json() == item_out


def test_item_patch_notfound():
    response = client.patch('/config/service/2/item/2',
                            {'name': 'Test Item 2'})
    assert response.status_code == 404


def test_item_delete():
    response = client.delete('/config/service/2/item/1')
    assert response.status_code == 200
    assert response.json() == item_out
    service_out["items"] = []


def test_item_delete_notfound():
    response = client.delete('/config/service/2/item/1')
    assert response.status_code == 404

# endregion


def test_delete():
    response = client.delete('/config/service/2')
    assert response.status_code == 200
    assert response.json() == service_out


def test_delete_notfound():
    response = client.delete('/config/service/3')
    assert response.status_code == 404
