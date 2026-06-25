import os

import camelot
from pypdf import PdfReader

from utils_future.file.File import File


class PDFFile(File):

    def get_text_lines(self) -> list[str]:
        lines = []
        reader = PdfReader(self.path)
        for page in reader.pages:
            text = page.extract_text() or ""
            lines.extend(line for line in text.splitlines() if line.strip())
        return lines

    def build_raw_tables(self, dir_tables: str) -> list[str]:
        os.makedirs(dir_tables, exist_ok=True)
        tables = camelot.read_pdf(
            self.path,
            pages="all",
            flavor="lattice",
            line_scale=40,
            strip_text="\n",
        )
        tables = sorted(
            tables,
            key=lambda t: (t.page, -t._bbox[3], t._bbox[0]),
        )

        tsv_paths = []
        for i, table in enumerate(tables):
            tsv_path = os.path.join(dir_tables, f"{i}.tsv")
            table.df.to_csv(tsv_path, sep="\t", index=False, header=False)
            tsv_paths.append(tsv_path)
        return tsv_paths
