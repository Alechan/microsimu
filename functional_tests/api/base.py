from urllib.parse import urljoin

LAWM_OUTPUT_VARIABLES = {
    'capd_5', 'exlife', 'birthr', 'calor', 'rlfd_3', 'gnpd_5', 'prot', 'capd_3', 'falu', 'capd_2',
    'hsexfl', 'rlfd_2', 'pop', 'excal', 'gnpd_1', 'enrol', 'rlfd_1', 'popr', 'tlf', 'capd_4', 'rlfd_5', 'al',
    'gnpd_2', '_11_70', 'grmor', 'eapopr', 'gnp', 'turbh', 'gnpd_3', 'capt', 'houser', 'capd_1', 'gnpxc', '_6_17',
    'urbanr', 'rlfd_4', 'rend', 'sepopr', 'chmor', 'educr', '_0_5', 'fert', 'perxfl', 'gnpd_4'
}

SIMULATIONS_ENDPOINT_URL = "/api/simulations/"
SIMULATE_ENDPOINT_URL    = "/api/simulate/"


def get_simulations_from_api(api_url, request_session):
    simulations_url = urljoin(api_url, SIMULATIONS_ENDPOINT_URL)
    simulations_raw = request_session.get(simulations_url)
    assert simulations_raw
    simulations = simulations_raw.json()
    return simulations
