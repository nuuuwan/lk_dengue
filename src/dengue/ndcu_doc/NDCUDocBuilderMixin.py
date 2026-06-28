class NDCUDocBuilderMixin:

    def build(self, temp_pdf_file):
        self.write_metadata()
        self.write_pdf(temp_pdf_file)
        self.build_raw_tables()
        self.build_custom_data()
