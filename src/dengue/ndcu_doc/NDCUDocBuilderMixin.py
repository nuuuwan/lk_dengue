from abc import abstractmethod


class NDCUDocBuilderMixin:
    @abstractmethod
    def build_custom_data(self):
        pass

    def build(self, temp_pdf_file):
        self.build_metadata()
        self.build_pdf(temp_pdf_file)
        self.build_raw_tables()
        self.build_custom_data()
