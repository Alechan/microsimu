from copy import deepcopy
from datetime import timezone, datetime
from urllib.parse import urljoin

from requests.auth import HTTPBasicAuth

from functional_tests.api.base import SIMULATE_ENDPOINT_URL, get_simulations_from_api, SIMULATIONS_ENDPOINT_URL

SIMULATION_STOP_VALUE = 2050


def test_simulate(wait_for_api):
    """
    Test that simulation runs can be triggered correctly

    :param wait_for_api: a fixture defined in fixtures.py
    :return:
    """
    request_session, api_url = wait_for_api
    simulate_url = urljoin(api_url, SIMULATE_ENDPOINT_URL)
    # As a user of the API,
    # I want to get the parameters of a model
    get_response_simulate = request_session.get(simulate_url)
    default_parameters = assert_simulate_valid_get_response(get_response_simulate)
    # If I don't provide auth data, I want the POST request to return an error
    assert_simulate_valid_post_response_not_logged_in(request_session, simulate_url)
    # I want to be able to send authenticated OPTIONS requests
    assert_simulate_valid_options_response(request_session, simulate_url)
    # I want to be able to send authenticated POST requests
    expected_redirect_relative_url = get_expected_redirect_relative_url(api_url, request_session)
    before_creation_time = datetime.now(timezone.utc)
    post_response_simulate = make_authenticated_post_to_simulate(request_session, simulate_url, default_parameters)
    after_creation_time = datetime.now(timezone.utc)
    # I expect that the redirect takes me to the detail of this simulation
    assert post_response_simulate.headers['Location'] == expected_redirect_relative_url
    # I follow the redirect and get the new simulation detail data
    redirections = list(request_session.resolve_redirects(post_response_simulate, post_response_simulate.request))
    assert len(redirections) == 1
    new_simu_detail = redirections[0].json()
    # I expect that the new simulation was created with the right creation time
    created_time_iso = new_simu_detail["created"]
    created_time_datetime = datetime.fromisoformat(created_time_iso)
    assert before_creation_time <= created_time_datetime <= after_creation_time
    # I expect that the new simulation shows the parameters I set
    actual_simulation_stop = new_simu_detail["parameters"]["general"]["simulation_stop"]
    assert SIMULATION_STOP_VALUE == actual_simulation_stop


def assert_simulate_valid_options_response(request_session, simulate_url):
    http_auth = get_valid_http_auth()
    options_response_simulate = request_session.options(simulate_url, allow_redirects=False, auth=http_auth)
    assert options_response_simulate.status_code == 200
    # I expect the authenticated OPTIONS request to include information about the parameters
    simulate_metadata = options_response_simulate.json()
    assert "actions" in simulate_metadata
    assert "POST" in simulate_metadata["actions"]
    assert "general" in simulate_metadata["actions"]["POST"]
    assert "simulation_stop" in simulate_metadata["actions"]["POST"]["general"]
    expected_param_fields = {"default", "description", "fortran_name", "maximum", "minimum", "name", "unit"}
    assert expected_param_fields == simulate_metadata["actions"]["POST"]["general"]["simulation_stop"].keys()


def get_expected_redirect_relative_url(api_url, request_session):
    simulations_before = get_simulations_from_api(api_url, request_session)
    expected_new_simu_id = len(simulations_before) + 1
    expected_redirect_relative_url = f"{SIMULATIONS_ENDPOINT_URL}{expected_new_simu_id}/"
    return expected_redirect_relative_url


def make_authenticated_post_to_simulate(request_session, simulate_url, default_parameters):
    params = deepcopy(default_parameters)
    params["general"]["simulation_stop"] = SIMULATION_STOP_VALUE
    http_auth = get_valid_http_auth()
    post_response_simulate = request_session.post(simulate_url, json=params, allow_redirects=False, auth=http_auth)
    expected_status_code = 302
    assert post_response_simulate.status_code == expected_status_code
    return post_response_simulate


def get_valid_http_auth():
    http_auth = HTTPBasicAuth('funct_test_user', 'plsdonthack')
    return http_auth


def assert_simulate_valid_post_response_not_logged_in(request_session, simulations_url):
    post_response_simulate = request_session.post(simulations_url, {"simulation_stop": 2001}, allow_redirects=False)
    assert post_response_simulate.status_code == 403


def assert_simulate_valid_get_response(get_response_simulate):
    assert get_response_simulate
    default_parameters = get_response_simulate.json()
    actual_params_categories = default_parameters.keys()
    expected_params_categories = {"regional", "general"}
    assert expected_params_categories == actual_params_categories
    return default_parameters
