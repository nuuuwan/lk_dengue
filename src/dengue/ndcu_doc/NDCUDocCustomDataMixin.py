import os
from abc import abstractmethod

from utils_future import Log

log = Log("NDCUDocCustomDataMixin")


class NDCUDocCustomDataMixin:
    @property
    def dir_custom_data(self) -> str:
        dir_custom_data = os.path.join(self.dir_data, "custom_data")
        os.makedirs(dir_custom_data, exist_ok=True)
        return dir_custom_data

    @abstractmethod
    def build_custom_data(self):
        pass
