import os
from abc import ABC
from dataclasses import dataclass


@dataclass
class NDCUDocBase(ABC):
    date_str: str
    pdf_url: str

    def __str__(self):
        return f"{self.__class__.__name__}({self.date_str})"

    @property
    def year_str(self) -> str:
        return self.date_str[:4]

    @property
    def month_str(self) -> str:
        return self.date_str[:7]

    @classmethod
    def get_dir_class(cls) -> str:
        dir_class = os.path.join("data", cls.__name__)
        os.makedirs(dir_class, exist_ok=True)
        return dir_class

    @property
    def dir_data(self) -> str:
        dir_data = os.path.join(
            self.get_dir_class(),
            self.year_str,
            self.month_str,
            self.date_str,
        )
        os.makedirs(dir_data, exist_ok=True)
        return dir_data

    @property
    def to_dict(self) -> dict:
        return {
            "date_str": self.date_str,
            "pdf_url": self.pdf_url,
        }
