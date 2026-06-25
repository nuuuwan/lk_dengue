import os

from utils_future import File, Log, Parse, TSVFile

log = Log("NDCUWeeklyDeathsByAgeAndSexMixin")


class NDCUWeeklyDeathsByAgeAndSexMixin:

    @property
    def deaths_by_age_and_sex_file(self) -> str:
        return TSVFile(
            os.path.join(self.dir_custom_data, "deaths_by_age_and_sex.tsv")
        )

    def _get_deaths_by_age_and_sex_raw_content(self):
        for file_name in sorted(os.listdir(self.dir_tables)):
            if file_name.endswith(".tsv"):
                content = File(
                    os.path.join(self.dir_tables, file_name)
                ).read()
                if "[age & sex]" in content.lower():
                    return content
        raise ValueError("No file with age and sex raw data")

    def _build_deaths_by_age_and_sex_data(self):
        content = self._get_deaths_by_age_and_sex_raw_content()
        data_list = []

        for line in content.splitlines():
            tokens = line.split("\t")
            if len(tokens) != 6:
                continue
            age_group_1 = tokens[0].strip()

            if "-" not in age_group_1:
                continue

            n_deaths_male_1 = Parse.int(tokens[1])
            n_deaths_female_1 = Parse.int(tokens[2])

            age_group_2 = tokens[3].strip()
            n_deaths_male_2 = Parse.int(tokens[4])
            n_deaths_female_2 = Parse.int(tokens[5])

            data_1 = dict(
                age_group=age_group_1,
                n_deaths_male=n_deaths_male_1,
                n_deaths_female=n_deaths_female_1,
            )

            data_2 = dict(
                age_group=age_group_2,
                n_deaths_male=n_deaths_male_2,
                n_deaths_female=n_deaths_female_2,
            )

            data_list.extend([data_1, data_2])

        data_list.sort(key=lambda x: x["age_group"])
        self.deaths_by_age_and_sex_file.write(data_list)
        log.info(
            f"Wrote {len(data_list)} rows to {self.deaths_by_age_and_sex_file}"
        )
