class NDCUDocBuilderMixin:

    def build(self, force):
        self.build_raw_tables(force)
        self.build_custom_data(force)

    @classmethod
    def build_all(cls, force=False):
        docs = cls.list()
        for doc in docs:
            doc.build(force=force)
