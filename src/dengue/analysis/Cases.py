from dengue.ndcu_daily import NDCUDaily
from utils_future import Log

log = Log("Cases")


class Cases:

    @classmethod
    def by_district(cls):
        latest_daily = NDCUDaily.latest()
        cases_by_district = latest_daily.district_data_file.read()

        district_id_to_n_cases = {}
        for d in cases_by_district:
            district_id = d["district_id"][:5]
            n_cases = int(d["n_cases"])
            if district_id not in district_id_to_n_cases:
                district_id_to_n_cases[district_id] = 0
            district_id_to_n_cases[district_id] += n_cases

        return dict(
            date_str=latest_daily.date_str,
            district_id_to_n_cases=district_id_to_n_cases,
        )
