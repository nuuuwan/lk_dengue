import os

from utils_future import JSONFile, Log

log = Log("NDCUDocMetadataMixin")


class NDCUDocMetadataMixin:
    @property
    def metadata_file(self) -> str:
        return JSONFile(os.path.join(self.dir_data, "metadata.json"))

    def build_metadata(self, force=False):
        if not force and self.metadata_file.exists:
            log.debug(f"{self.metadata_file} exists")
            return
        self.metadata_file.write(self.to_dict)
        log.info(f"Wrote {self.metadata_file}")
