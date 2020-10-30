from urllib.parse import urljoin

from rest_framework import status

LAWM_OUTPUT_VARIABLES = {
    'capd_5', 'exlife', 'birthr', 'calor', 'rlfd_3', 'gnpd_5', 'prot', 'capd_3', 'falu', 'capd_2',
    'hsexfl', 'rlfd_2', 'pop', 'excal', 'gnpd_1', 'enrol', 'rlfd_1', 'popr', 'tlf', 'capd_4', 'rlfd_5', 'al',
    'gnpd_2', '_11_70', 'grmor', 'eapopr', 'gnp', 'turbh', 'gnpd_3', 'capt', 'houser', 'capd_1', 'gnpxc', '_6_17',
    'urbanr', 'rlfd_4', 'rend', 'sepopr', 'chmor', 'educr', '_0_5', 'fert', 'perxfl', 'gnpd_4'
}

def test_simulations_paths(wait_for_api):
    """
    Test that we can follow the urls returned by /simulations/ endpoint

    :param wait_for_api: a fixture defined in fixtures.py
    :return:
    """
    request_session, api_url = wait_for_api
    # As a user of the API,
    # I want to know what simulations results are currently available
    simulations_url = urljoin(api_url, "/api/simulations/")
    simulations_raw = request_session.get(simulations_url)
    assert simulations_raw.status_code == status.HTTP_200_OK
    simulations= simulations_raw.json()
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
