from dengue.ndcu_daily import NDCUDaily
from dengue.ndcu_weekly import NDCUWeekly
from utils_future import File, Log

log = Log("ReadMe")


class ReadMe:
    FILE = File("README.md")
    DOC_CLASS_LIST = [NDCUDaily, NDCUWeekly]

    def get_lines_for_source_reports(self) -> list[str]:
        lines = [
            "## Source Reports",
            "",
        ]
        for doc_class in self.DOC_CLASS_LIST:
            lines.extend(doc_class.get_lines_for_source_reports())
        return lines

    def build(self):
        lines = ["# Dengue in Sri Lanka 🇱🇰", ""]
        lines.extend(self.get_lines_for_source_reports())

        self.FILE.write("\n".join(lines))
        log.info(f"Wrote {self.FILE}")
