from dengue.analysis import Chart
from dengue.ndcu_daily import NDCUDaily
from dengue.ndcu_weekly import NDCUWeekly
from utils_future import File, Log, Time, TimeFormat

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
            "## Appendix: Source Reports",
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
        metric_color,
    ) -> list[str]:
        image_path = Chart.chart_metric_by_region(
            Doc=Doc,
            get_file_from_latest=get_file_from_latest,
            get_metric=get_metric,
            metric_label=metric_label,
            metric_color=metric_color,
        )
        lines = [
            f"## {metric_label}",
            "",
            f"![]({image_path})",
            "",
        ]

        lines.append("")
        return lines

    @staticmethod
    def get_lines_for_charts():
        for (
            Doc,
            get_file_from_latest,
            get_metric,
            metric_label,
            metric_color,
        ) in [
            (
                NDCUWeekly,
                lambda latest: latest.cases_by_district_file,
                lambda d: int(d["n_this_year_this_week"]),
                "Cases this week",
                "orange",
            ),
            (
                NDCUWeekly,
                lambda latest: latest.cases_by_district_file,
                lambda d: (
                    int(d["n_this_year_this_week"])
                    - int(d["n_this_year_last_week"])
                ),
                "Additional Cases this week (compared to Last Week)",
                "orange",
            ),
            (
                NDCUWeekly,
                lambda latest: latest.deaths_by_district_file,
                lambda d: int(d["n_deaths"]),
                "Cumulative Deaths in 2026",
                "darkred",
            ),
            (
                NDCUDaily,
                lambda latest: latest.district_data_file,
                lambda d: int(d["n_cases"]),
                "Cumulative Cases in 2026",
                "darkorange",
            ),
        ]:
            yield from ReadMe.get_lines_for_chart(
                Doc=Doc,
                get_file_from_latest=get_file_from_latest,
                get_metric=get_metric,
                metric_label=metric_label,
                metric_color=metric_color,
            )

    @staticmethod
    def build():
        lines = (
            ["# Dengue in Sri Lanka 🇱🇰", ""]
            + ReadMe.get_lines_for_header()
            + list(ReadMe.get_lines_for_charts())
            + ReadMe.get_lines_for_source_reports()
            + ReadMe.get_lines_for_footer()
        )

        ReadMe.FILE.write("\n".join(lines))
        log.info(f"Wrote {ReadMe.FILE}")
