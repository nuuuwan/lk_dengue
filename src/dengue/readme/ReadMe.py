from utils_future import File, Log

log = Log("ReadMe")


class ReadMe:
    FILE = File("README.md")

    def build(self):
        lines = ["# Dengue in Sri Lanka 🇱🇰", ""]
        self.FILE.write("\n".join(lines))
        log.info(f"Wrote {self.FILE}")
