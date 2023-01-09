from .test_1_main import client
from .test_4_service import service_in, service_out

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
    "icon": "fas fa-google",
    "subtitle": "subtitle",
    "url": "https://www.google.com"
}


def test_post_service():
    service_in['name'] = 'Test Service 1'
    service_out['name'] = 'Test Service 1'

    response = client.post('/config/service', service_in)
    assert response.status_code == 201
    assert response.json() == service_out


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
    assert response.status_code == 200
    item_out['name'] = 'Test Item 2'
    item_in['name'] = 'Test Item 2'
    assert response.json() == item_out


def test_item_patch_notfound():
    response = client.patch('/config/service/2/item/2',
                            {'name': 'Test Item 2'})
    assert response.status_code == 404


def test_put():
    item_in.pop('subtitle')
    item_out.pop('subtitle')

    response = client.put('/config/service/2/item/1', item_in)
    assert response.status_code == 200
    assert response.json() == item_out


def test_put_notfound():
    response = client.put('/config/service/2/item/2', item_in)
    assert response.status_code == 404


def test_item_delete():
    response = client.delete('/config/service/2/item/1')
    assert response.status_code == 200
    assert response.json() == item_out
    service_out["items"] = []


def test_item_delete_notfound():
    response = client.delete('/config/service/2/item/1')
    assert response.status_code == 404
