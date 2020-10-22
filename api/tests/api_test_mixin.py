from datetime import datetime, timedelta

from api.models.models import LAWMSimulation, LAWMResult


class ApiTestMixin:
    @staticmethod
    def create_simple_db_simulation(pop_values):
        simu = LAWMSimulation.objects.create()
        for val in pop_values:
            _ = LAWMResult.objects.create(
                pop=val,
                popr=4000,
                simulation=simu,
            )
        return simu

    @staticmethod
    def get_lawm_results_from_ids(ids):
        lawm_results = LAWMResult.objects.filter(pk__in=ids)
        return lawm_results

    def assert_is_later_and_close(self, after_time_iso, before_time_iso):
        self.assertGreater(after_time_iso, before_time_iso)
        actual_time   = datetime.fromisoformat(after_time_iso)
        expected_time = datetime.fromisoformat(before_time_iso)
        actual_timedelta = abs(actual_time - expected_time)
        max_timedelta = timedelta(seconds=10)
        if actual_timedelta > max_timedelta:
            self.fail(f"The expected time {expected_time} is not close to the actual time {actual_time}.")
