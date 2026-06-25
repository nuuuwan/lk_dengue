from dengue.ndcu_doc.NDCUDoc import NDCUDoc
from dengue.ndcu_weekly.NDCUWeeklyCasesByDistrictMixin import \
    NDCUWeeklyCasesByDistrictMixin
from dengue.ndcu_weekly.NDCUWeeklyDeathsByAgeAndSexMixin import \
    NDCUWeeklyDeathsByAgeAndSexMixin
from dengue.ndcu_weekly.NDCUWeeklyDeathsByDistrictMixin import \
    NDCUWeeklyDeathsByDistrictMixin
from dengue.ndcu_weekly.NDCUWeeklyHighRiskMOHAreasMixin import \
    NDCUWeeklyHighRiskMOHAreasMixin
from dengue.ndcu_weekly.NDCUWeeklySentinelHospitalsMixin import \
    NDCUWeeklySentinelHospitalsMixin
from utils_future import Log, TimeFormat

log = Log("NDCUWeekly")


class NDCUWeekly(
    NDCUDoc,
    NDCUWeeklyCasesByDistrictMixin,
    NDCUWeeklyHighRiskMOHAreasMixin,
    NDCUWeeklySentinelHospitalsMixin,
    NDCUWeeklyDeathsByAgeAndSexMixin,
    NDCUWeeklyDeathsByDistrictMixin,
):

    @classmethod
    def _parse_date_str(cls, lines: list[str]) -> str:
        for i_line, line in enumerate(lines):
            if line.strip().lower() == "weekly dengue update":
                date_line = lines[i_line + 1].strip().replace(")", "")
                tokens = date_line.split(" ")
                week_no = int(tokens[1])
                year = int(tokens[-1])
                date_str = TimeFormat.DATE.format(
                    TimeFormat("%Y %U %w").parse(f"{year} {week_no} 0")
                )
                return date_str
        raise ValueError("Could not find date_str")

    def build_custom_data(self):
        self._build_cases_by_district_data()
        self._build_high_risk_moh_areas_data()
        self._build_sentinel_hospitals_data()
        self._build_deaths_by_age_and_sex_data()
        self._build_deaths_by_district_data()
