import os

from utils_future import Log, TSVFile
from utils_future.RegionUtils import RegionUtils

log = Log("NDCUDailyDistrictMixin")


class NDCUDailyDistrictMixin:

    @property
    def district_data_file(self) -> str:
        return TSVFile(
            os.path.join(self.dir_custom_data, "district_data.tsv")
        )

    def _get_district_raw_tables(self) -> list[list[dict]]:
        tables = []
        for file_name in os.listdir(self.dir_tables):
            if file_name.endswith(".tsv"):
                table = TSVFile(
                    os.path.join(self.dir_tables, file_name)
                ).read()
                content = str(table)
                if "District" in content:
                    tables.append(table)

        return tables

    @staticmethod
    def __map_data(d: dict) -> dict:
        district_name = None
        n_cases = None
        for k, v in d.items():
            if "district" in k.lower():
                district_name = v
            elif "cases" in k.lower():
                n_cases = int(v)
        if not district_name or n_cases is None:
            return None

        district_id = RegionUtils.get_region_id_to_name(district_name)

        return dict(
            district_id=district_id,
            district_name=district_name,
            n_cases=n_cases,
        )

    def _build_district_data(self, force):
        if self.district_data_file.exists and not force:
            log.debug(f"{self.district_data_file} exists")
            return

        tables = self._get_district_raw_tables()
        log.debug(f"Found {len(tables)} district tables")

        data_list = []
        for d in tables[0] + tables[1]:
            data = self.__map_data(d)
            if data is not None:
                data_list.append(data)

        data_list.sort(key=lambda x: x["district_id"])

        self.district_data_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.district_data_file.path}"
        )
