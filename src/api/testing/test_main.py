import httpx

class Client:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get(self, path: str, headers = None):
        if headers == None:
            headers = self.headers

        return httpx.get(f'{self.base_url}{path}', headers=headers)

    def post(self, path: str, json: dict, headers = None):
        if headers == None:
            headers = self.headers

        return httpx.post(f'{self.base_url}{path}', json=json, headers=headers)

    def patch(self, path: str, json: dict, headers = None):
        if headers == None:
            headers = self.headers

        return httpx.patch(f'{self.base_url}{path}', json=json, headers=headers)

    def put(self, path: str, headers = None):
        if headers == None:
            headers = self.headers

        return httpx.put(f'{self.base_url}{path}', headers=headers)

    def delete(self, path: str, headers = None):
        if headers == None:
            headers = self.headers

        return httpx.delete(f'{self.base_url}{path}', headers=headers)

client = Client('http://localhost:8000', {'Authorization': 'Bearer 1234'})

def test_ping():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}