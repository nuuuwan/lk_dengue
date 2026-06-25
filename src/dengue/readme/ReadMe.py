from dengue.analysis import Chart, Deaths
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
    def get_lines_for_deaths() -> list[str]:
        deaths_by_district = Deaths.by_district()
        deaths_by_district_image_path = Chart.chart_metric_by_region(
            date_str=deaths_by_district["date_str"],
            id_to_metric=deaths_by_district["district_id_to_n_deaths"],
            metric_label="deaths",
        )
        lines = [
            "## Deaths in 2026",
            "",
            f"![]({deaths_by_district_image_path})",
            "",
        ]

        lines.append("")
        return lines

    @staticmethod
    def build():
        lines = (
            ["# Dengue in Sri Lanka 🇱🇰", ""]
            + ReadMe.get_lines_for_header()
            + ReadMe.get_lines_for_deaths()
            + ReadMe.get_lines_for_source_reports()
            + ReadMe.get_lines_for_footer()
        )

        ReadMe.FILE.write("\n".join(lines))
        log.info(f"Wrote {ReadMe.FILE}")
