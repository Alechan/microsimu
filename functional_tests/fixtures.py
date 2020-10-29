import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

pytest_plugins = ["docker_compose"]

container_name = "web"


@pytest.fixture(scope="session")
def wait_for_api(session_scoped_container_getter):
    """
    Invoking pytest fixture 'session_scoped_container_getter' starts all
    docker services for the entire session.

    :param session_scoped_container_getter: fixture provided by pytest-docker-compose
    :return:
    """
    request_session = get_request_session()

    service_url = get_service_url(session_scoped_container_getter)
    assert request_session.get(service_url), "The service is not up or the root url is not valid."
    return request_session, service_url


def get_service_url(container_getter):
    service = container_getter.get(container_name).network_info[0]
    api_url = f"http://{service.hostname}:{service.host_port}/"
    return api_url


def get_request_session():
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))
    return request_session
