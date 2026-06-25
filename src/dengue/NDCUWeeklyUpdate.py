from dengue.NDCUDoc import NDCUDoc
from utils_future import Log, TimeFormat

log = Log("NDCUWeeklyUpdate")


class NDCUWeeklyUpdate(NDCUDoc):

    @classmethod
    def _parse_date_str(cls, lines: list[str]) -> str:
        for i_line, line in enumerate(lines):
            if line.strip().lower() == "weekly dengue update":
                date_line = lines[i_line + 1].strip().replace(")", "")
                tokens = date_line.split(" ")
                week_no = int(tokens[1])
                year = int(tokens[-1])
                date_str = TimeFormat.DATE.format(
                    TimeFormat("%Y %U %w").parse(f"{year} {week_no} 0")
                )
                return date_str
        raise ValueError("Could not find date_str")
