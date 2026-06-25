import os

from dengue.ndcu_doc.NDCUDoc import NDCUDoc
from utils_future import Log, TimeFormat, TSVFile

log = Log("NDCUDailyUpdate")


class NDCUDailyUpdate(NDCUDoc):

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

    @property
    def district_data_file(self) -> str:
        return TSVFile(os.path.join(self.dir_data, "district_data.tsv"))

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
                data = dict(
                    district_name=district_name,
                    n_cases=n_cases,
                )
                data_list.append(data)

        self.district_data_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.district_data_file.path}"
        )

    def build_custom_data(self, force=False):
        self._build_district_data(force)
