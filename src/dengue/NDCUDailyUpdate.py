import os
import shutil
import tempfile
from dataclasses import dataclass

from utils_future import WWW, Log, PDFFile, TimeFormat

log = Log("NDCUDailyUpdate")


@dataclass
class NDCUDailyUpdate:
    date_str: str
    pdf_url: str

    def __str__(self):
        return f"NDCUDailyUpdate({self.pdf_url})"

    @property
    def year_str(self) -> str:
        return self.date_str[:4]

    @property
    def month_str(self) -> str:
        return self.date_str[:7]

    @property
    def dir_data(self) -> str:
        dir_data = os.path.join(
            "data",
            "ndcu_daily_updates",
            self.year_str,
            self.month_str,
            self.date_str,
        )
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    @property
    def pdf_file(self) -> PDFFile:
        return PDFFile(os.path.join(self.dir_data, "original.pdf"))

    @property
    def to_dict(self) -> dict:
        return {
            "date_str": self.date_str,
            "pdf_url": self.pdf_url,
        }

    @staticmethod
    def _parse_date_str(lines: list[str]) -> str:
        for line in lines:
            if "as of" in line.lower():
                date_str = (
                    line.lower()
                    .split("as of")[-1]
                    .strip()
                    .split(" ")[0]
                    .strip()
                )
                date_str = TimeFormat.DATE.format(
                    TimeFormat("%d.%m.%Y").parse(date_str)
                )
                return date_str
        raise ValueError("Could not find date_str")

    @classmethod
    def from_pdf_url(cls, pdf_url: str):
        log.debug(f"{pdf_url=}")
        temp_dir = os.path.join(tempfile.gettempdir(), "dengue")
        os.makedirs(temp_dir, exist_ok=True)
        temp_pdf_file = PDFFile(
            os.path.join(temp_dir, os.path.basename(pdf_url))
        )
        WWW(pdf_url).download_binary(temp_pdf_file.path)
        log.debug(f"Downloaded {pdf_url} to {temp_pdf_file}")
        date_str = cls._parse_date_str(temp_pdf_file.get_text_lines())
        self = cls(date_str=date_str, pdf_url=pdf_url)

        shutil.copy(
            temp_pdf_file.path,
            self.pdf_file.path,
        )
        log.info(f"Wrote {self.pdf_file}")
        return self
