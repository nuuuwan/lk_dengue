import os

from utils_future import File, Log, Parse, RegionUtils, TSVFile

log = Log("NDCUWeeklyHighRiskMOHAreasMixin")


class NDCUWeeklyHighRiskMOHAreasMixin:

    @property
    def high_risk_moh_areas_file(self) -> str:
        return TSVFile(os.path.join(self.dir_data, "high_risk_moh_areas.tsv"))

    def _get_high_risk_moh_areas_raw_content(self):
        contents = []
        for file_name in sorted(os.listdir(self.dir_tables)):
            if file_name.endswith(".tsv"):
                content = File(
                    os.path.join(self.dir_tables, file_name)
                ).read()
                if "cases reported" in content.lower():
                    contents.append(content)
        return "\n".join(contents)

    def _build_high_risk_moh_areas_data(self):
        content = self._get_high_risk_moh_areas_raw_content()
        data_list = []

        district_name = None
        for line in content.splitlines():
            tokens = line.split("\t")
            if len(tokens) != 3:
                continue
            moh_area_name = tokens[0].strip().replace("*", "")

            if (
                not moh_area_name.strip()
                or "total" in moh_area_name.lower()
                or "moh area" in moh_area_name.lower()
            ):
                continue

            if "district" in moh_area_name.lower():
                district_name = (
                    moh_area_name.lower()
                    .replace("district", "")
                    .strip()
                    .title()
                )
                continue

            if "province" in moh_area_name.lower():

                continue

            if tokens[1] == "" and tokens[2] == "":
                tokens0_tokens1 = tokens[0].split()
                if len(tokens0_tokens1) >= 3:
                    moh_area_name = " ".join(tokens0_tokens1[:-2])
                    tokens[1] = tokens0_tokens1[-2]
                    tokens[2] = tokens0_tokens1[-1]

            n_cases_last_week = Parse.int(tokens[1])
            n_cases_this_week = Parse.int(tokens[2])
            data = dict(
                district_id=RegionUtils.get_region_id_from_name(
                    district_name
                ),
                district_name=district_name,
                moh_area_name=moh_area_name,
                n_cases_last_week=n_cases_last_week,
                n_cases_this_week=n_cases_this_week,
            )
            data_list.append(data)

        data_list.sort(
            key=lambda x: (str(x["district_id"]), x["moh_area_name"])
        )
        self.high_risk_moh_areas_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.high_risk_moh_areas_file}"
        )
