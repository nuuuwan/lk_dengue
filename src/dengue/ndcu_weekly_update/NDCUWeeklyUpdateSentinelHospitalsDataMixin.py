import os

from utils_future import File, Log, Parse, TSVFile

log = Log("NDCUWeeklyUpdateHighRiskMOHAreasDataMixin")


class NDCUWeeklyUpdateSentinelHospitalsDataMixin:

    @property
    def sentinel_hospitals_file(self) -> str:
        return TSVFile(os.path.join(self.dir_data, "sentinel_hospitals.tsv"))

    def _get_sentinel_hospitals_raw_content(self):
        contents = []
        for file_name in sorted(os.listdir(self.dir_tables)):
            if file_name.endswith(".tsv"):
                content = File(
                    os.path.join(self.dir_tables, file_name)
                ).read()
                if "average midnight total" in content.lower():
                    contents.append(content)
        return "\n".join(contents)

    def _build_sentinel_hospitals_data(self):
        content = self._get_sentinel_hospitals_raw_content()
        data_list = []

        for line in content.splitlines():
            tokens = line.split("\t")
            print(len(tokens), tokens)
            if len(tokens) != 4:
                continue
            hospital_name = tokens[0].strip().replace("*", "")

            if "average midnight total" in hospital_name.lower():
                continue

            n_cases_last_week = Parse.int(tokens[1])
            n_cases_this_week = Parse.int(tokens[2])
            data = dict(
                hospital_name=hospital_name,
                n_cases_last_week=n_cases_last_week,
                n_cases_this_week=n_cases_this_week,
            )
            data_list.append(data)

        data_list.sort(key=lambda x: x["hospital_name"])
        self.sentinel_hospitals_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.sentinel_hospitals_file}"
        )
