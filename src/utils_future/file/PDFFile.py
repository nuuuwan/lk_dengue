from pypdf import PdfReader

from utils_future.file.File import File


class PDFFile(File):
    pass

    def get_text_lines(self) -> list[str]:
        lines = []
        reader = PdfReader(self.path)
        for page in reader.pages:
            text = page.extract_text() or ""
            lines.extend(line for line in text.splitlines() if line.strip())
        return lines
