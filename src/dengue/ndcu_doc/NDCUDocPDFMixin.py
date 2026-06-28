import os
import shutil
import tempfile

from utils_future import WWW, Log, PDFFile

log = Log("NDCUDocPDFMixin")


class NDCUDocPDFMixin:
    @property
    def pdf_file(self) -> PDFFile:
        return PDFFile(os.path.join(self.dir_data, "original.pdf"))

    def write_pdf(self, temp_pdf_file, force=False):
        if self.pdf_file.exists:
            return

        shutil.copy(
            temp_pdf_file.path,
            self.pdf_file.path,
        )
        log.info(f"Wrote {self.pdf_file}")

    @staticmethod
    def _download_pdf(pdf_url):
        temp_dir = os.path.join(tempfile.gettempdir(), "dengue")
        os.makedirs(temp_dir, exist_ok=True)
        temp_pdf_file = PDFFile(
            os.path.join(temp_dir, os.path.basename(pdf_url))
        )
        WWW(pdf_url).download_binary(temp_pdf_file.path)
        log.debug(f"Downloaded {pdf_url} to {temp_pdf_file}")
        return temp_pdf_file
