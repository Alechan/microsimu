import requests

server_url = "http://localhost:8000"


def test_get_locations_for_us_90210_check_status_code_equals_200():
    response = requests.get(server_url)
    assert response.status_code == 200

