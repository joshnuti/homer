from .test_1_main import client
from .test_4_service import service_in, service_out

custom_item_in = {
    "order": 6,
    "name": "Portainer",
    "icon": "fas fa-server",
    "url": "https://192.168.2.156:9443/",
    "type": "Portainer",
    "apikey": "5555",
    "environments": ['local']
}

custom_item_out = {
    "id": 1,
    "order": 6,
    "name": "Portainer",
    "icon": "fas fa-server",
    "url": "https://192.168.2.156:9443/",
    "type": "Portainer",
    "apikey": "5555",
    "environments": ['local']
}


def test_customitem_post():
    response = client.post('/config/service/2/item', custom_item_in)
    assert response.status_code == 201
    assert response.json() == custom_item_out
    service_out["items"].append(custom_item_out)


def test_customitem_post_conflict():
    response = client.post('/config/service/2/item', custom_item_in)
    assert response.status_code == 409


def test_get_withcustomitem():
    response = client.get('/config/service/2')
    assert response.status_code == 200
    assert response.json() == service_out


def test_customitem_get():
    response = client.get('/config/service/2/item/1')
    assert response.status_code == 200
    assert response.json() == custom_item_out


def test_customitem_get_notfound1():
    response = client.get('/config/service/2/item/2')
    assert response.status_code == 404


def test_customitem_get_notfound2():
    response = client.get('/config/service/3/item/2')
    assert response.status_code == 404


def test_customitem_patch():
    response = client.patch('/config/service/2/item/1',
                            {'name': 'Portainer 2'})
    assert response.status_code == 200
    custom_item_out["name"] = 'Portainer 2'
    assert response.json() == custom_item_out


def test_customitem_patch_notfound():
    response = client.patch('/config/service/2/item/2',
                            {'name': 'Portainer 2'})
    assert response.status_code == 404


def test_customitem_delete():
    response = client.delete('/config/service/2/item/1')
    assert response.status_code == 200
    assert response.json() == custom_item_out
    service_out["items"] = []


def test_customitem_delete_notfound():
    response = client.delete('/config/service/2/item/1')
    assert response.status_code == 404
