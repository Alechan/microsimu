from datetime import timezone, datetime
from urllib.parse import urljoin

import pytest
from requests.auth import HTTPBasicAuth

from functional_tests.api.base import SIMULATE_ENDPOINT_URL, get_simulations_from_api, SIMULATIONS_ENDPOINT_URL


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
    assert_simulate_valid_get_response(get_response_simulate)
    # If I'm not logged in, I want the POST request to return an error
    assert_simulate_valid_post_response_not_logged_in(request_session, simulate_url)
    # I want to be able to send authenticated POST requests
    # (in real life, don't include the password in the command, wait for the prompt)
    # I want to be able to trigger simulations run with user defined parameters
    before_creation_time = datetime.now(timezone.utc)
    default_params = get_default_params()
    post_response_simulate = request_session.post(simulate_url, json=default_params, allow_redirects=False, auth=HTTPBasicAuth('funct_test_user', 'plsdonthack'))
    after_creation_time = datetime.now(timezone.utc)
    expected_status_code = 302
    assert post_response_simulate.status_code   == expected_status_code
    # I expect that the redirect takes me to the detail of this simulation
    simulations_before = get_simulations_from_api(api_url, request_session)
    expected_new_simu_id = len(simulations_before) + 1
    expected_redirect_relative_url = f"{SIMULATIONS_ENDPOINT_URL}{expected_new_simu_id}/"
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
    assert False, "terminame"


def assert_simulate_valid_post_response_not_logged_in(request_session, simulations_url):
    post_response_simulate = request_session.post(simulations_url, {"simulation_stop": 2001}, allow_redirects=False)
    assert post_response_simulate.status_code == 403


def assert_simulate_valid_get_response(get_response_simulate):
    assert get_response_simulate
    parameters = get_response_simulate.json()
    actual_params_categories = parameters.keys()
    expected_params_categories = {"regional", "general"}
    assert expected_params_categories == actual_params_categories

def get_default_params():
    return {
        "general": {
            "simulation_stop": 2000,
            "optimization_start": 1980,
            "payments_equilibrium": 2000,
            "fertilizer_cost": 769230.8,
            "weight_constraint_1": 6.0,
            "weight_constraint_2": 8.0,
            "weight_constraint_3": 6.0,
            "weight_constraint_4": 6.0,
            "weight_constraint_5": 6.0,
            "weight_constraint_6": 6.0,
            "weight_constraint_7": 4.0,
            "weight_constraint_8": 4.0,
            "weight_constraint_9": 6.0,
            "weight_constraint_10": 6.0,
            "weight_constraint_11": 6.0,
            "weight_constraint_12": 2.0,
            "weight_constraint_13": 4.0,
            "weight_constraint_14": 4.0,
            "weight_constraint_15": 7.0,
            "weight_constraint_16": 4.0,
            "weight_constraint_17": 4.0,
            "weight_constraint_18": 4.0,
            "weight_constraint_19": 8.0,
            "weight_constraint_20": 6.0,
            "weight_constraint_21": 4.0,
            "weight_constraint_22": 6.0,
            "weight_constraint_23": 8.0,
            "weight_constraint_24": 6.0,
            "weight_constraint_25": 2.0,
            "weight_constraint_26": 1.0
        },
        "regional": {
            "developed": {
                "max_calories": 3200.0,
                "max_build_cost": 10.0,
                "tech_prog_coeff_1": 1.01,
                "tech_prog_coeff_2": 1.01,
                "tech_prog_coeff_3": 1.005,
                "tech_prog_coeff_4": 1.01,
                "tech_prog_coeff_5": 1.015,
                "tech_prog_stop": 3000.0,
                "years_building_cost_eq": 40,
                "years_housing_level_eq": 10,
                "desired_food_stock": 365.0,
                "years_space_p_person_eq": 40,
                "max_space_p_person": 30.0,
                "desired_space_p_person": 30.0,
                "max_sec_5_gnp_propor": 0.25
            },
            "latinamerica": {
                "max_calories": 3000.0,
                "max_build_cost": 7.0,
                "tech_prog_coeff_1": 1.01,
                "tech_prog_coeff_2": 1.01,
                "tech_prog_coeff_3": 1.005,
                "tech_prog_coeff_4": 1.01,
                "tech_prog_coeff_5": 1.015,
                "tech_prog_stop": 3000.0,
                "years_building_cost_eq": 40,
                "years_housing_level_eq": 10,
                "desired_food_stock": 365.0,
                "years_space_p_person_eq": 40,
                "max_space_p_person": 30.0,
                "desired_space_p_person": 10.0,
                "max_sec_5_gnp_propor": 0.25
            },
            "africa": {
                "max_calories": 3000.0,
                "max_build_cost": 7.0,
                "tech_prog_coeff_1": 1.01,
                "tech_prog_coeff_2": 1.01,
                "tech_prog_coeff_3": 1.005,
                "tech_prog_coeff_4": 1.01,
                "tech_prog_coeff_5": 1.015,
                "tech_prog_stop": 3000.0,
                "years_building_cost_eq": 40,
                "years_housing_level_eq": 20,
                "desired_food_stock": 365.0,
                "years_space_p_person_eq": 40,
                "max_space_p_person": 30.0,
                "desired_space_p_person": 7.0,
                "max_sec_5_gnp_propor": 0.25
            },
            "asia": {
                "max_calories": 3000.0,
                "max_build_cost": 7.0,
                "tech_prog_coeff_1": 1.01,
                "tech_prog_coeff_2": 1.01,
                "tech_prog_coeff_3": 1.005,
                "tech_prog_coeff_4": 1.01,
                "tech_prog_coeff_5": 1.015,
                "tech_prog_stop": 3000.0,
                "years_building_cost_eq": 40,
                "years_housing_level_eq": 20,
                "desired_food_stock": 365.0,
                "years_space_p_person_eq": 40,
                "max_space_p_person": 30.0,
                "desired_space_p_person": 7.0,
                "max_sec_5_gnp_propor": 0.25
            }
        }
    }
