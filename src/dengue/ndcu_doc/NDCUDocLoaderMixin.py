import os
from abc import abstractmethod

from utils_future import JSONFile, Log

log = Log("NDCUDocLoaderMixin")


class NDCUDocLoaderMixin:
    @classmethod
    def from_dict(cls, d):
        return cls(date_str=d["date_str"], pdf_url=d["pdf_url"])

    @classmethod
    def from_pdf_url_hot(cls, pdf_url: str, force=False):
        self = cls.from_pdf_url(pdf_url)
        if self is not None and not force:
            log.debug(f"{self} exists")
            return self

        temp_pdf_file = cls._download_pdf(pdf_url)
        date_str = cls._parse_date_str(temp_pdf_file.get_text_lines())
        self = cls(date_str=date_str, pdf_url=pdf_url)
        self.build(temp_pdf_file)
        return self

    @classmethod
    @abstractmethod
    def _parse_date_str(cls, lines: list[str]) -> str:
        pass

    @classmethod
    def list(cls):
        docs = []
        for dir_year in os.listdir(cls.get_dir_class()):
            for dir_month in os.listdir(
                os.path.join(cls.get_dir_class(), dir_year)
            ):
                for dir_date in os.listdir(
                    os.path.join(cls.get_dir_class(), dir_year, dir_month)
                ):
                    metadata_file_path = os.path.join(
                        cls.get_dir_class(),
                        dir_year,
                        dir_month,
                        dir_date,
                        "metadata.json",
                    )
                    if os.path.exists(metadata_file_path):
                        d = JSONFile(metadata_file_path).read()
                        doc = cls.from_dict(d)
                        docs.append(doc)
        docs.sort(key=lambda doc: doc.date_str, reverse=True)
        return docs

    @classmethod
    def from_pdf_url(cls, pdf_url: str):
        docs = cls.list()
        for doc in docs:
            if doc.pdf_url == pdf_url:
                doc.build(doc.pdf_file)
                return doc
        return None
