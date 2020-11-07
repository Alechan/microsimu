from datetime import timezone, datetime
from urllib.parse import urljoin

import pytest

from functional_tests.api.base import SIMULATE_ENDPOINT_URL, get_simulations_from_api, SIMULATIONS_ENDPOINT_URL


@pytest.mark.skip(reason="Simulate endpoint POST request not finished yet")
def test_simulate(wait_for_api):
    """
    Test that simulation runs can be triggered correctly

    :param wait_for_api: a fixture defined in fixtures.py
    :return:
    """
    request_session, api_url = wait_for_api
    simulations_url = urljoin(api_url, SIMULATE_ENDPOINT_URL)
    # As a user of the API,
    # I want to get the parameters of a model
    get_response_simulate = request_session.get(simulations_url)
    assert get_response_simulate
    parameters = get_response_simulate.json()
    all_params_names = parameters.keys()
    assert len(all_params_names) > 0
    # Get the simulations to know how many were there were before
    simulations = get_simulations_from_api(api_url, request_session)
    # I want to be able to trigger simulations run with user defined parameters
    before_creation_time = datetime.now(timezone.utc)
    get_response_simulate = request_session.post(simulations_url, {"simulation_stop": 2001}, allow_redirects=False)
    after_creation_time = datetime.now(timezone.utc)
    expected_status_code = 302
    assert get_response_simulate.status_code         == expected_status_code
    # I expect that the redirect takes me to the detail of this simulation
    expected_new_simu_id = len(simulations) + 1
    expected_redirect_relative_url = f"{SIMULATIONS_ENDPOINT_URL}{expected_new_simu_id}/"
    assert get_response_simulate.headers['Location'] == expected_redirect_relative_url
    # I follow the redirect and get the new simulation detail data
    redirections = list(request_session.resolve_redirects(get_response_simulate, get_response_simulate.request))
    assert len(redirections) == 1
    new_simu_detail = redirections[0].json()
    # I expect that the new simulation was created with the right creation time
    created_time_iso = new_simu_detail["created"]
    created_time_datetime = datetime.fromisoformat(created_time_iso)
    assert before_creation_time <= created_time_datetime <= after_creation_time
    # I expect that the new simulation shows the parameters I set
    assert False, "terminame"
