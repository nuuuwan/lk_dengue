from dengue.ndcu_daily import NDCUDaily
from dengue.ndcu_weekly import NDCUWeekly
from utils_future import File, Log

log = Log("ReadMe")


class ReadMe:
    FILE = File("README.md")

    def get_lines_for_source_reports(self) -> list[str]:
        lines = [
            "## Source Reports",
            "",
        ]
        lines.extend(NDCUDaily.get_lines_for_source_reports())
        lines.extend(NDCUWeekly.get_lines_for_source_reports())
        return lines

    def build(self):
        lines = ["# Dengue in Sri Lanka 🇱🇰", ""]
        lines.extend(self.get_lines_for_source_reports())

        self.FILE.write("\n".join(lines))
        log.info(f"Wrote {self.FILE}")
