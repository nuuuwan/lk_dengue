import os

from utils_future import File, Log, Parse, RegionUtils, TSVFile

log = Log("NDCUWeeklyDeathsByDistrictMixin")


class NDCUWeeklyDeathsByDistrictMixin:

    @property
    def deaths_by_district_file(self) -> str:
        return TSVFile(
            os.path.join(self.dir_custom_data, "deaths_by_district.tsv")
        )

    def _get_deaths_by_district_raw_content(self):
        for file_name in sorted(os.listdir(self.dir_tables)):
            if file_name.endswith(".tsv"):
                content = File(
                    os.path.join(self.dir_tables, file_name)
                ).read()
                if "deaths reported in 2026 [districts" in content.lower():
                    return content
        raise ValueError("No file with deaths by district raw data")

    def _build_deaths_by_district_data(self, force):
        if self.deaths_by_district_file.exists and not force:
            log.debug(f"{self.deaths_by_district_file} exists")
            return
        content = self._get_deaths_by_district_raw_content()
        data_list = []

        for line in content.splitlines()[2:]:
            tokens = line.split("\t")
            for i_col in range(3):
                district_name = tokens[i_col * 2].strip()
                if not district_name:
                    continue
                district_id = RegionUtils.get_region_id_from_name(
                    district_name
                )
                n_deaths = Parse.int(tokens[i_col * 2 + 1])
                data = dict(
                    district_id=district_id,
                    district_name=district_name,
                    n_deaths=n_deaths,
                )
                data_list.append(data)

        data_list.sort(key=lambda x: x["district_id"])
        self.deaths_by_district_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.deaths_by_district_file}"
        )
