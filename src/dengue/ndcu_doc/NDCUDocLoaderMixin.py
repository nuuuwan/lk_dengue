from abc import abstractmethod

from utils_future import Log

log = Log("NDCUDocLoaderMixin")


class NDCUDocLoaderMixin:
    @classmethod
    def from_pdf_url(cls, pdf_url: str):
        log.debug(f"{pdf_url=}")
        temp_pdf_file = cls._download_pdf(pdf_url)
        date_str = cls._parse_date_str(temp_pdf_file.get_text_lines())
        self = cls(date_str=date_str, pdf_url=pdf_url)
        self.build(temp_pdf_file)
        return self

    @classmethod
    @abstractmethod
    def _parse_date_str(cls, pdf_text_lines: list[str]) -> str:
        pass
