from dengue.analysis import Chart, ChartMOH
from dengue.ndcu_daily import NDCUDaily
from dengue.ndcu_weekly import NDCUWeekly
from moh import MOH
from utils_future import File, Log, Markdown, Time, TimeFormat

log = Log("ReadMe")


class ReadMe:
    FILE = File("README.md")
    DOC_CLASS_LIST = [NDCUDaily, NDCUWeekly]

    @staticmethod
    def get_lines_for_header() -> list[str]:
        time_str = TimeFormat.DATE.format(Time.now())
        time_str = time_str.replace("-", "--").replace(" ", "_")
        return [
            "![Last Updated](https://img.shields.io/badge/"
            + f"last_updated-{time_str}-green)",
            "",
        ]

    @staticmethod
    def get_lines_for_footer() -> list[str]:
        return [
            "![Maintainer]"
            + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
            "![MadeWith](https://img.shields.io/badge/made_with-python-blue)",
            "[![License: MIT]"
            + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
            + "(https://opensource.org/licenses/MIT)",
            "",
        ]

    @staticmethod
    def get_lines_for_source_reports() -> list[str]:
        lines = [
            "## Appendix: Source Reports & Extracted Data",
            "",
        ]
        for doc_class in ReadMe.DOC_CLASS_LIST:
            lines.extend(doc_class.get_lines_for_source_reports())
        return lines

    @staticmethod
    def get_lines_for_chart(
        Doc,
        get_file_from_latest,
        get_metric,
        metric_label,
        positive_color,
        negative_color,
    ) -> list[str]:
        image_path = Chart.chart_metric_by_region(
            Doc=Doc,
            get_file_from_latest=get_file_from_latest,
            get_metric=get_metric,
            metric_label=metric_label,
            positive_color=positive_color,
            negative_color=negative_color,
        )
        lines = [
            f"## {metric_label}",
            "",
            f"![{metric_label}]({image_path})",
            "",
        ]

        return lines

    @staticmethod
    def get_lines_for_charts():
        for (
            Doc,
            get_file_from_latest,
            get_metric,
            metric_label,
            positive_color,
            negative_color,
        ) in [
            (
                NDCUWeekly,
                lambda latest: latest.cases_by_district_file,
                lambda d: int(d["n_this_year_this_week"]),
                "Cases this week",
                "orange",
                "white",
            ),
            (
                NDCUWeekly,
                lambda latest: latest.cases_by_district_file,
                lambda d: (
                    int(d["n_this_year_this_week"])
                    - int(d["n_this_year_last_week"])
                ),
                "Additional Cases this week (compared to last week)",
                "orange",
                "white",
            ),
            (
                NDCUWeekly,
                lambda latest: latest.cases_by_district_file,
                lambda d: (
                    int(d["n_this_year_this_week"])
                    - int(d["n_last_year_this_week"])
                ),
                "Additional Cases this week (compared to this week, last year)",
                "orange",
                "white",
            ),
            (
                NDCUWeekly,
                lambda latest: latest.deaths_by_district_file,
                lambda d: int(d["n_deaths"]),
                "Cumulative Deaths in 2026",
                "darkred",
                "white",
            ),
            (
                NDCUDaily,
                lambda latest: latest.district_data_file,
                lambda d: int(d["n_cases"]),
                "Cumulative Cases in 2026",
                "darkorange",
                "white",
            ),
        ]:
            yield from ReadMe.get_lines_for_chart(
                Doc=Doc,
                get_file_from_latest=get_file_from_latest,
                get_metric=get_metric,
                metric_label=metric_label,
                positive_color=positive_color,
                negative_color=negative_color,
            )

    @staticmethod
    def get_lines_for_chart_moh() -> list[str]:
        image_path = ChartMOH.chart_metric_by_moh(
            Doc=NDCUWeekly,
            get_file_from_latest=(
                lambda latest: latest.high_risk_moh_areas_file
            ),
            get_metric=lambda d: int(d["n_cases_this_week"]),
            metric_label="Cases this week by MOH Region",
            positive_color="orange",
            negative_color="white",
        )
        return [
            "## Cases this week by MOH Region",
            "",
            f"![Cases this week by MOH Region]({image_path})",
            "",
        ]

    @staticmethod
    def get_lines_for_tables_moh_regions() -> list[str]:
        latest = NDCUWeekly.latest()
        lines = [
            "## Cases by MOH Regions",
            "",
            f"As of {latest.date_str}",
            "",
        ]

        d_list = latest.high_risk_moh_areas_file.read()

        def ramap(d):
            n_cases_last_week = int(d["n_cases_last_week"])
            n_cases_this_week = int(d["n_cases_this_week"])

            moh = MOH.from_name_fuzzy(d["moh_area_name"])

            return {
                "ID": moh.region_id if moh else "⚠️ Unknown",
                "District": d["district_name"],
                "MOH Area": d["moh_area_name"],
                "Cases Last Week": n_cases_last_week,
                "Cases This Week": n_cases_this_week,
            }

        d_list = [ramap(d) for d in d_list]
        d_list = [d for d in d_list if d["Cases This Week"] > 0]
        d_list.sort(
            key=lambda x: (
                -x["Cases This Week"],
                x["District"],
                x["MOH Area"],
            )
        )

        lines.append(Markdown.table(d_list))
        return lines

    @staticmethod
    def get_lines_for_tables_hospitals() -> list[str]:
        latest = NDCUWeekly.latest()
        lines = [
            "## Cases by Hospitals",
            "",
            f"As of {latest.date_str}",
            "",
        ]

        d_list = latest.sentinel_hospitals_file.read()

        def ramap(d):
            n_cases_last_week = int(d["n_cases_last_week"])
            n_cases_this_week = int(d["n_cases_this_week"])

            return {
                "Hospital": d["hospital_name"],
                "Cases Last Week": n_cases_last_week,
                "Cases This Week": n_cases_this_week,
            }

        d_list = [ramap(d) for d in d_list]
        d_list = [d for d in d_list if d["Cases This Week"] > 0]
        d_list.sort(
            key=lambda x: (
                -x["Cases This Week"],
                x["Hospital"],
            )
        )

        lines.append(Markdown.table(d_list))
        return lines

    @staticmethod
    def get_lines_for_tables() -> list[str]:
        return (
            ReadMe.get_lines_for_tables_moh_regions()
            + ReadMe.get_lines_for_tables_hospitals()
        )

    @staticmethod
    def build():
        lines = (
            [
                "# Dengue in Sri Lanka 🇱🇰",
                "",
            ]
            + ReadMe.get_lines_for_header()
            + [
                "Datasets scraped from"
                + " [National Dengue Control Unit]"
                + "(https://www.dengue.health.gov.lk/) Website.",
                "",
            ]
            + list(ReadMe.get_lines_for_charts())
            + ReadMe.get_lines_for_chart_moh()
            + ReadMe.get_lines_for_tables()
            + ReadMe.get_lines_for_source_reports()
            + ReadMe.get_lines_for_footer()
        )

        ReadMe.FILE.write("\n".join(lines))
        log.info(f"Wrote {ReadMe.FILE}")
