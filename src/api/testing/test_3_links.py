from .test_1_main import client

link_in = {
    "order": 5,
    "name": "Test Link 1",
    "url": "https://www.google.com",
    "icon": "fas fa-google",
    "target": "#"
}

link_out = {
    "id": 3,
    "order": 5,
    "name": "Test Link 1",
    "url": "https://www.google.com",
    "icon": "fas fa-google",
    "target": "#"
}


def test_get():
    response = client.get("/config/link")
    assert response.status_code == 200


def test_get_invalid():
    response = client.get('/config/link', {})
    assert response.status_code == 403


def test_post():
    response = client.post('/config/link', link_in)
    assert response.status_code == 201
    assert response.json() == link_out


def test_post_conflict():
    response = client.post('/config/link', link_in)
    assert response.status_code == 409


def test_get_specific():
    response = client.get('/config/link/3')
    assert response.status_code == 200
    assert response.json() == link_out


def test_get_specific_notfound():
    response = client.get('/config/link/4')
    assert response.status_code == 404


def test_patch():
    response = client.patch('/config/link/3', {'name': 'Test Link 2'})
    assert response.status_code == 200
    link_in['name'] = 'Test Link 2'
    link_out['name'] = 'Test Link 2'
    assert response.json() == link_out


def test_patch_notfound():
    response = client.patch('/config/link/4', {'name': 'Test Link 2'})
    assert response.status_code == 404


def test_put():
    link_in.pop('target')
    link_out.pop('target')

    response = client.put('/config/link/3', link_in)
    assert response.status_code == 200
    assert response.json() == link_out


def test_put_notfound():
    response = client.put('/config/link/4', link_in)
    assert response.status_code == 404


def test_delete():
    response = client.delete('/config/link/3')
    assert response.status_code == 200
    assert response.json() == link_out


def test_delete_notfound():
    response = client.delete('/config/link/3')
    assert response.status_code == 404
