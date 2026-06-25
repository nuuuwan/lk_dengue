from dengue.ndcu_weekly import NDCUWeekly
from utils_future import Log

log = Log("Deaths")


class Deaths:

    @classmethod
    def by_district(cls):
        latest_weekly = NDCUWeekly.latest()
        deaths_by_district = latest_weekly.deaths_by_district_file.read()

        district_id_to_n_deaths = {}
        for d in deaths_by_district:
            district_id = d["district_id"][:5]
            n_deaths = int(d["n_deaths"])
            if district_id not in district_id_to_n_deaths:
                district_id_to_n_deaths[district_id] = 0
            district_id_to_n_deaths[district_id] += n_deaths

        return dict(
            date_str=latest_weekly.date_str,
            district_id_to_n_deaths=district_id_to_n_deaths,
        )
