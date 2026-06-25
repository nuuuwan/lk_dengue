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

    def _has_custom_data(self) -> bool:
        if not os.path.exists(self.dir_custom_data):
            return False
        for file_name in os.listdir(self.dir_custom_data):
            if file_name.endswith(".tsv"):
                return True
        return False

    @abstractmethod
    def build_custom_data_inner(self):
        pass

    def build_custom_data(self, force=False):
        if self._has_custom_data() and not force:
            log.debug(f"{self.dir_custom_data} exists")
            return
        self.build_custom_data_inner()
