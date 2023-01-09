from .test_1_main import client


def test_reset_config():
    response = client.put('/config/defaults')
    assert response.status_code == 201


def test_get_config_invalid():
    response = client.get('/config', {})
    assert response.status_code == 403


def test_get_config():
    response = client.get("/config")
    assert response.status_code == 200


def test_patch_config():
    response = client.patch('/config', {'title': 'Test Title'})
    assert response.status_code == 201
    assert response.json()['title'] == 'Test Title'
