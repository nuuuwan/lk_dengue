import os

from utils_future import JSONFile, Log

log = Log("NDCUDocMetadataMixin")


class NDCUDocMetadataMixin:
    @property
    def metadata_file(self) -> str:
        return JSONFile(os.path.join(self.dir_data, "metadata.json"))

    def build_metadata(self):
        self.metadata_file.write(self.to_dict)
        log.info(f"Wrote {self.metadata_file}")
