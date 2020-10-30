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

    container = session_scoped_container_getter.get(container_name)
    service = container.network_info[0]
    api_url = f"http://{service.hostname}:{service.host_port}/"
    if not request_session.get(api_url):
        base_msg = f"The service is not up or the root url is not valid."
        url      = f"The url used was {api_url}"
        service_hostname       = f"service.hostname: {service.hostname}"
        service_host_port      = f"service.host_port: {service.host_port}"
        service_container_port = f"service.container_port: {service.container_port}"
        error_msg = "\n".join([base_msg, url, service_hostname, service_host_port, service_container_port])
        assert False, error_msg
    return request_session, api_url


def get_request_session():
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))
    return request_session
