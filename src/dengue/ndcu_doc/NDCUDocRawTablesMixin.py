import os

from utils_future import Log

log = Log("NDCUDocRawTablesMixin")


class NDCUDocRawTablesMixin:
    def dir_tables(self) -> str:
        dir_tables = os.path.join(self.dir_data, "raw_tables")
        os.makedirs(dir_tables, exist_ok=True)
        return dir_tables

    def build_raw_tables(self, force=True):
        dir_tables = self.dir_tables()
        if os.path.exists(dir_tables) and not force:
            log.debug(f"{dir_tables} exists")
            return
        self.pdf_file.build_raw_tables(dir_tables)
