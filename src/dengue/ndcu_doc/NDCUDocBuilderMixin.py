from utils_future import Log

log = Log("NDCUDocBuilderMixin")


class NDCUDocBuilderMixin:

    def build(self, force):
        self.build_raw_tables(force)
        self.build_custom_data(force)

    @classmethod
    def build_all(cls, force=False):
        docs = cls.list()
        n = len(docs)
        for i_doc, doc in enumerate(docs, start=1):
            log.debug("-" * 32)
            log.debug(f"{i_doc}/{n} Building {doc}")
            log.debug("-" * 32)
            doc.build(force=force)
