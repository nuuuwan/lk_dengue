import os

from moh import MOH
from utils_future import File, Log, Parse, RegionUtils, TSVFile

log = Log("NDCUWeeklyHighRiskMOHAreasMixin")


class NDCUWeeklyHighRiskMOHAreasMixin:

    @property
    def high_risk_moh_areas_file(self) -> str:
        return TSVFile(
            os.path.join(self.dir_custom_data, "high_risk_moh_areas.tsv")
        )

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

    # flake8: noqa: C901
    @staticmethod
    def __parse_line(line, district_name):
        tokens = line.split("\t")
        if len(tokens) != 3:
            return None, district_name
        moh_area_name = tokens[0].strip().replace("*", "")

        if (
            not moh_area_name.strip()
            or "province" in moh_area_name.lower()
            or "total" in moh_area_name.lower()
            or "moh area" in moh_area_name.lower()
        ):
            return None, district_name

        if "district" in moh_area_name.lower():
            district_name = (
                moh_area_name.lower().replace("district", "").strip().title()
            )
            return None, district_name

        if tokens[1] == "" and tokens[2] == "":
            tokens0_tokens1 = tokens[0].split()
            if len(tokens0_tokens1) >= 3:
                moh_area_name = " ".join(tokens0_tokens1[:-2])
                tokens[1] = tokens0_tokens1[-2]
                tokens[2] = tokens0_tokens1[-1]

        n_cases_last_week = Parse.int(tokens[1])
        n_cases_this_week = Parse.int(tokens[2])
        data = dict(
            district_id=RegionUtils.get_region_id_from_name(district_name),
            district_name=district_name,
            moh_area_name=moh_area_name,
            n_cases_last_week=n_cases_last_week,
            n_cases_this_week=n_cases_this_week,
        )
        return data, district_name

    def _normalize(self, data_list):
        # map
        moh_to_data_list = {}
        for d in data_list:
            moh_name = d["moh_area_name"].upper()
            moh = MOH.from_name_fuzzy(moh_name)
            if not moh:
                log.warning(f"Could not find MOH for {moh_name}")
                continue
            moh_id = moh.region_id
            if moh_id not in moh_to_data_list:
                moh_to_data_list[moh_id] = []
            moh_to_data_list[moh_id].append(d)

        # reduce
        aggr_data_list = []
        for moh_id, d_list in moh_to_data_list.items():
            moh = MOH.from_id(moh_id)
            d = dict(
                moh_id=moh_id,
                moh_area_name=" & ".join(
                    sorted([d["moh_area_name"] for d in d_list])
                ),
                district_id=moh.district_id,
                district_name=d_list[0]["district_name"],
                n_cases_last_week=sum(d["n_cases_last_week"] for d in d_list),
                n_cases_this_week=sum(d["n_cases_this_week"] for d in d_list),
                population=moh.population,
                n_cases_last_week_per_100k=(
                    sum(d["n_cases_last_week"] for d in d_list)
                    / moh.population
                    * 100_000
                ),
                n_cases_this_week_per_100k=(
                    sum(d["n_cases_this_week"] for d in d_list)
                    / moh.population
                    * 100_000
                ),
            )
            aggr_data_list.append(d)
        aggr_data_list.sort(
            key=lambda x: (str(x["district_id"]), x["moh_area_name"])
        )
        return aggr_data_list

    def _build_high_risk_moh_areas_data(self, force):
        if self.high_risk_moh_areas_file.exists and not force:
            log.debug(f"{self.high_risk_moh_areas_file} exists")
            return
        content = self._get_high_risk_moh_areas_raw_content()
        data_list = []

        district_name = None
        for line in content.splitlines():
            data, district_name = self.__parse_line(line, district_name)
            if data is not None:
                data_list.append(data)

        data_list = self._normalize(data_list)
        self.high_risk_moh_areas_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.high_risk_moh_areas_file}"
        )
