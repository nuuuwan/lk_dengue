import os

from utils_future import Log, TSVFile

log = Log("NDCUDailyUpdateDistrictDataMixin")


class NDCUDailyUpdateDistrictDataMixin:
    @staticmethod
    def _get_district_id_from_name(district_name: str) -> str:
        district_name = {
            "Monaragala": "Moneragala",
            "Nuwaraeliya": "Nuwara Eliya",
        }.get(district_name, district_name)
        return {
            "Colombo": "LK-11",
            "Gampaha": "LK-12",
            "Kalutara": "LK-13",
            "Kandy": "LK-21",
            "Matale": "LK-22",
            "Nuwara Eliya": "LK-23",
            "Galle": "LK-31",
            "Matara": "LK-32",
            "Hambantota": "LK-33",
            "Jaffna": "LK-41",
            "Kilinochchi": "LK-42",
            "Mannar": "LK-43",
            "Vavuniya": "LK-44",
            "Mullaitivu": "LK-45",
            "Batticaloa": "LK-51",
            "Ampara": "LK-52",
            "Trincomalee": "LK-53",
            "Kurunegala": "LK-61",
            "Puttalam": "LK-62",
            "Anuradhapura": "LK-71",
            "Polonnaruwa": "LK-72",
            "Badulla": "LK-81",
            "Moneragala": "LK-82",
            "Ratnapura": "LK-91",
            "Kegalle": "LK-92",
            #
            "CMC": "LK-11-CMC",
            "NIHS": "LK-13-NIHS",
            "Kalmunai": "LK-52-Kalmunai",
        }.get(district_name, district_name)

    @property
    def district_data_file(self) -> str:
        return TSVFile(os.path.join(self.dir_data, "district_data.tsv"))

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

    def _build_district_data(self, force):
        if self.district_data_file.exists and not force:
            log.debug(f"{self.district_data_file} exists")
            return

        tables = self._get_district_raw_tables()
        log.debug(f"Found {len(tables)} district tables")

        data_list = []
        for d in tables[0] + tables[1]:
            district_name = None
            n_cases = None
            for k, v in d.items():
                if "district" in k.lower():
                    district_name = v
                elif "cases" in k.lower():
                    n_cases = int(v)
            if district_name and n_cases is not None:
                district_id = self._get_district_id_from_name(district_name)

                data = dict(
                    district_id=district_id,
                    district_name=district_name,
                    n_cases=n_cases,
                )
                data_list.append(data)

        data_list.sort(key=lambda x: x["district_id"])

        self.district_data_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.district_data_file.path}"
        )
