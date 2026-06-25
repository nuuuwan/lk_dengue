from dengue.ndcu_daily import NDCUDaily
from dengue.ndcu_weekly import NDCUWeekly
from utils_future import Log

log = Log("Cases")


class Cases:

    @classmethod
    def cum2026_cases_by_district(cls):
        latest_daily = NDCUDaily.latest()
        d_list = latest_daily.district_data_file.read()

        id_to_n = {}
        for d in d_list:
            region_id = d["district_id"][:5]
            n = int(d["n_cases"])
            if region_id not in id_to_n:
                id_to_n[region_id] = 0
            id_to_n[region_id] += n

        return dict(
            date_str=latest_daily.date_str,
            district_id_to_n_cases=id_to_n,
        )

    @classmethod
    def cases_this_week_by_district(cls):
        latest_weekly = NDCUWeekly.latest()
        d_list = latest_weekly.cases_by_district_file.read()

        id_to_n = {}
        for d in d_list:
            region_id = d["district_id"][:5]
            n = int(d["n_this_year_this_week"])
            if region_id not in id_to_n:
                id_to_n[region_id] = 0
            id_to_n[region_id] += n

        return dict(
            date_str=latest_weekly.date_str,
            district_id_to_n_cases=id_to_n,
        )
