from dengue.ndcu_daily.NDCUDailyDistrictMixin import NDCUDailyDistrictMixin
from dengue.ndcu_doc.NDCUDoc import NDCUDoc
from utils_future import Log, TimeFormat

log = Log("NDCUDaily")


class NDCUDaily(NDCUDoc, NDCUDailyDistrictMixin):

    @classmethod
    def get_full_name(cls) -> str:
        return "National Dengue Control Unit - Daily Update"

    @classmethod
    def _parse_date_str(cls, lines: list[str]) -> str:
        for line in lines:
            if "as of" in line.lower():
                date_str = (
                    line.lower()
                    .split("as of")[-1]
                    .strip()
                    .split(" ")[0]
                    .strip()
                )
                date_str = TimeFormat.DATE.format(
                    TimeFormat("%d.%m.%Y").parse(date_str)
                )
                return date_str
        raise ValueError("Could not find date_str")

    def build_custom_data(self, force=False):
        self._build_district_data(force)
