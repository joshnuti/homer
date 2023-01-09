from .test_1_main import client

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
    assert response.status_code == 200
    service_in['name'] = 'Test Service 2'
    service_out['name'] = 'Test Service 2'
    assert response.json() == service_out


def test_patch_notfound():
    response = client.patch('/config/service/3', {'name': 'Test Service 2'})
    assert response.status_code == 404


def test_put():
    service_in.pop('icon')
    service_out.pop('icon')

    response = client.put('/config/service/2', service_in)
    assert response.status_code == 200
    assert response.json() == service_out


def test_put_notfound():
    response = client.put('/config/service/3', service_in)
    assert response.status_code == 404


def test_delete():
    response = client.delete('/config/service/2')
    assert response.status_code == 200
    assert response.json() == service_out


def test_delete_notfound():
    response = client.delete('/config/service/3')
    assert response.status_code == 404
