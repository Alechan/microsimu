from datetime import timezone, datetime
from urllib.parse import urljoin

LAWM_OUTPUT_VARIABLES = {
    'capd_5', 'exlife', 'birthr', 'calor', 'rlfd_3', 'gnpd_5', 'prot', 'capd_3', 'falu', 'capd_2',
    'hsexfl', 'rlfd_2', 'pop', 'excal', 'gnpd_1', 'enrol', 'rlfd_1', 'popr', 'tlf', 'capd_4', 'rlfd_5', 'al',
    'gnpd_2', '_11_70', 'grmor', 'eapopr', 'gnp', 'turbh', 'gnpd_3', 'capt', 'houser', 'capd_1', 'gnpxc', '_6_17',
    'urbanr', 'rlfd_4', 'rend', 'sepopr', 'chmor', 'educr', '_0_5', 'fert', 'perxfl', 'gnpd_4'
}

SIMULATE_ENDPOINT_URL    = "/api/simulate/"
SIMULATIONS_ENDPOINT_URL = "/api/simulations/"


def test_simulations_paths(wait_for_api):
    """
    Test that we can follow the urls returned by /simulations/ endpoint

    :param wait_for_api: a fixture defined in fixtures.py
    :return:
    """
    request_session, api_url = wait_for_api
    # As a user of the API,
    # I want to know what simulations results are currently available
    simulations = get_simulations_from_api(api_url, request_session)
    # The microservice should always at least have the LAWM standard run
    assert len(simulations) >= 1
    # I expect the list view of the first simulation to have the following fields
    first_simulation = simulations[0]
    expected_simu_list_fields = {"url", "created"}
    assert expected_simu_list_fields == first_simulation.keys()
    # I want to get the data for the first simulation, and I need the "url" field
    simu_1_url = first_simulation["url"]
    simu_1_detail_raw = request_session.get(simu_1_url)
    assert simu_1_detail_raw
    # I expect the first simulation detail to have the following fields
    simu_1_detail = simu_1_detail_raw.json()
    expected_simu_detail_fields = {"url", "regions", "created"}
    assert expected_simu_detail_fields == simu_1_detail.keys()
    # I expect that the regions included are the default
    regions = simu_1_detail["regions"]
    expected_regions_names = {"developed", "latinamerica", "africa", "asia"}
    actual_regions_names = regions.keys()
    assert expected_regions_names == actual_regions_names
    # For each region, I want to get their results
    regions_to_iterate = expected_regions_names.copy()
    for region_name in actual_regions_names:
        region_detail_url = regions[region_name]
        region_detail_raw = request_session.get(region_detail_url)
        assert region_detail_raw
        region_detail = region_detail_raw.json()
        # I expect the region to have the following fields
        expected_region_detail_fields = {'region', 'simulation', 'variables', 'results'}
        assert expected_region_detail_fields == region_detail.keys()
        # I expect the linked simulation to be the same one that got me here
        assert simu_1_url == region_detail["simulation"]
        # I expect it includes information for all variables
        assert LAWM_OUTPUT_VARIABLES == region_detail["variables"].keys()
        # I expect each variable information json object to have the following fields
        expected_variable_info_fields = {"name", "fortran_name", "unit", "description", "category"}
        for var_info in region_detail["variables"].values():
            assert expected_variable_info_fields == var_info.keys()
        # I expect the results to include all the years of the standard run
        actual_years   = [y_result["year"] for y_result in region_detail["results"]]
        expected_years = list(range(1960, 2001))
        assert expected_years == actual_years
        # I expect each result to include the year and the same variables from the variables information
        results_keys = LAWM_OUTPUT_VARIABLES.copy()
        results_keys.add("year")
        for y_result in region_detail["results"]:
            assert results_keys == y_result.keys()
        # I expect the region name to be one of the expected ones
        region_name = region_detail["region"]
        assert region_name in regions_to_iterate
        regions_to_iterate.remove(region_name)
    # Assert I iterated through all regions
    assert len(regions_to_iterate) == 0


def test_simulations_post(wait_for_api):
    """
    Test that simulation runs can be triggered correctly

    :param wait_for_api: a fixture defined in fixtures.py
    :return:
    """
    request_session, api_url = wait_for_api
    # Get the simulations to know how many were there were before
    simulations = get_simulations_from_api(api_url, request_session)
    # As a user of the API,
    # I want to be able to trigger simulations run with user defined parameters
    simulations_url = urljoin(api_url, SIMULATE_ENDPOINT_URL)
    before_creation_time = datetime.now(timezone.utc)
    response = request_session.post(simulations_url, {"simulation_stop": 2001}, allow_redirects=False)
    after_creation_time = datetime.now(timezone.utc)
    expected_status_code = 302
    assert response.status_code         == expected_status_code
    # I expect that the redirect takes me to the detail of this simulation
    expected_new_simu_id = len(simulations) + 1
    expected_redirect_relative_url = f"{SIMULATIONS_ENDPOINT_URL}{expected_new_simu_id}/"
    assert response.headers['Location'] == expected_redirect_relative_url
    # I follow the redirect and get the new simulation detail data
    redirections = list(request_session.resolve_redirects(response, response.request))
    assert len(redirections) == 1
    new_simu_detail = redirections[0].json()
    # I expect that the new simulation was created with the right creation time
    created_time_iso = new_simu_detail["created"]
    created_time_datetime = datetime.fromisoformat(created_time_iso)
    assert before_creation_time <= created_time_datetime <= after_creation_time
    # I expect that the new simulation shows the parameters I set


def get_simulations_from_api(api_url, request_session):
    simulations_url = urljoin(api_url, SIMULATIONS_ENDPOINT_URL)
    simulations_raw = request_session.get(simulations_url)
    assert simulations_raw
    simulations = simulations_raw.json()
    return simulations


