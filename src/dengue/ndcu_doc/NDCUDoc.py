from dengue.ndcu_doc.NDCUDocBase import NDCUDocBase
from dengue.ndcu_doc.NDCUDocBuilderMixin import NDCUDocBuilderMixin
from dengue.ndcu_doc.NDCUDocLoaderMixin import NDCUDocLoaderMixin
from dengue.ndcu_doc.NDCUDocMetadataMixin import NDCUDocMetadataMixin
from dengue.ndcu_doc.NDCUDocPDFMixin import NDCUDocPDFMixin
from dengue.ndcu_doc.NDCUDocRawTablesMixin import NDCUDocRawTablesMixin


class NDCUDocReadMeMixin:
    @classmethod
    def get_lines_for_source_reports(cls) -> list[str]:
        lines = [
            f"### [{cls.get_full_name()}]({cls.get_dir_class()})",
            "",
        ]
        docs = cls.list()
        for doc in docs:
            lines.append(f"- [{doc.date_str}]({doc.pdf_file.path})")
        if docs:
            lines.append("")
        return lines


class NDCUDoc(
    NDCUDocBase,
    #
    NDCUDocLoaderMixin,
    NDCUDocBuilderMixin,
    #
    NDCUDocMetadataMixin,
    NDCUDocPDFMixin,
    NDCUDocRawTablesMixin,
    #
    NDCUDocReadMeMixin,
):
    pass
