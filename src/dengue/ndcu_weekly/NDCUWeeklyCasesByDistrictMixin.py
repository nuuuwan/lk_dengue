import os

from utils_future import File, Log, Parse, RegionUtils, TSVFile

log = Log("NDCUWeeklyCasesByDistrictMixin")


class NDCUWeeklyCasesByDistrictMixin:
    @property
    def cases_by_district_file(self) -> str:
        return TSVFile(
            os.path.join(self.dir_custom_data, "cases_by_district.tsv")
        )

    def _get_cases_by_district_raw_table(self):
        for file_name in os.listdir(self.dir_tables):
            if file_name.endswith(".tsv"):
                content = File(
                    os.path.join(self.dir_tables, file_name)
                ).read()
                if "No. of cases" in content:
                    return content

        raise ValueError("Could not find cases_by_district table")

    def _build_cases_by_district_data(self, force):
        if self.cases_by_district_file.exists and not force:
            log.debug(f"{self.cases_by_district_file} exists")
            return
        content = self._get_cases_by_district_raw_table()
        data_list = []
        for line in content.splitlines()[4:]:
            tokens = line.split("\t")
            district_name = tokens[0].strip().replace("*", "")
            if district_name == "Total":
                continue
            n_last_year_last_week = Parse.int(tokens[1])
            n_last_year_this_week = Parse.int(tokens[2])
            n_this_year_last_week = Parse.int(tokens[3])
            n_this_year_this_week = Parse.int(tokens[4])
            cum_n_last_year = Parse.int(tokens[5])
            cum_n_this_year = Parse.int(tokens[6])

            district_id = RegionUtils.get_region_id_from_name(district_name)
            data = dict(
                district_id=district_id,
                district_name=district_name,
                n_last_year_last_week=n_last_year_last_week,
                n_last_year_this_week=n_last_year_this_week,
                n_this_year_last_week=n_this_year_last_week,
                n_this_year_this_week=n_this_year_this_week,
                cum_n_last_year=cum_n_last_year,
                cum_n_this_year=cum_n_this_year,
            )
            data_list.append(data)
        data_list.sort(key=lambda x: x["district_id"])
        self.cases_by_district_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.cases_by_district_file}"
        )
