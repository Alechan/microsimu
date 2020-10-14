import requests

server_url = "http://localhost:8000"


def test_main_url_returns_200_with_get():
    response = requests.get(server_url)
    assert response.status_code == 200

