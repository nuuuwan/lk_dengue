class NDCUDocBuilderMixin:
    def build(self, temp_pdf_file):
        self.build_metadata()
        self.build_pdf(temp_pdf_file)
        self.build_tables()
