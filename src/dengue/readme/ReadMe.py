from dengue.ndcu_daily import NDCUDaily
from dengue.ndcu_weekly import NDCUWeekly
from utils_future import File, Log, Time, TimeFormat

log = Log("ReadMe")


class ReadMe:
    FILE = File("README.md")
    DOC_CLASS_LIST = [NDCUDaily, NDCUWeekly]

    @staticmethod
    def get_lines_for_header() -> list[str]:
        # ![LastUpdated](https://img.shields.io/badge/last_updated-2026--06--25_06:58:43-green)
        time_str = TimeFormat.TIME.format(Time.now())
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
    def build():
        lines = (
            ["# Dengue in Sri Lanka 🇱🇰", ""]
            + ReadMe.get_lines_for_header()
            + ReadMe.get_lines_for_source_reports()
            + ReadMe.get_lines_for_footer()
        )

        ReadMe.FILE.write("\n".join(lines))
        log.info(f"Wrote {ReadMe.FILE}")
