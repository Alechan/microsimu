from urllib.parse import urljoin

from rest_framework import status


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
    # I expect the list view of the first simulation to include the following fields
    first_simulation = simulations[0]
    expected_simu_list_fields = {"url", "created"}
    assert keys_are_included_in_dict(expected_simu_list_fields, first_simulation)
    # I want to get the data for the first simulation, and I need the "url" field
    simu_1_url = first_simulation["url"]
    simu_1_detail_raw = request_session.get(simu_1_url)
    assert simu_1_detail_raw
    # I expect the first simulation detail to include the following fields
    simu_1_detail = simu_1_detail_raw.json()
    expected_simu_detail_fields = {"url", "regions", "created"}
    assert keys_are_included_in_dict(expected_simu_detail_fields, simu_1_detail)
    # I expect that the regions included are the default
    regions = simu_1_detail["regions"]
    expected_regions_names = {"developed", "latinamerica", "africa", "asia"}
    actual_regions_names = regions.keys()
    assert expected_regions_names == actual_regions_names
    # For each region, I want to get their results
    for region_name in actual_regions_names:
        region_detail_url = regions[region_name]
        assert request_session.get(region_detail_url)


def keys_are_included_in_dict(expected_keys, dictionary):
    actual_simu_list_fields = dictionary.keys()
    return set_is_included(expected_keys, actual_simu_list_fields)


def set_is_included(first, second):
    return first == (first & second)
