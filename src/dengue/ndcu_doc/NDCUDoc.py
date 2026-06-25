from dengue.ndcu_doc.NDCUDocBase import NDCUDocBase
from dengue.ndcu_doc.NDCUDocBuilderMixin import NDCUDocBuilderMixin
from dengue.ndcu_doc.NDCUDocLoaderMixin import NDCUDocLoaderMixin
from dengue.ndcu_doc.NDCUDocMetadataMixin import NDCUDocMetadataMixin
from dengue.ndcu_doc.NDCUDocPDFMixin import NDCUDocPDFMixin
from utils_future import Log

log = Log("NDCUDoc")


class NDCUDoc(
    NDCUDocBase,
    NDCUDocLoaderMixin,
    NDCUDocBuilderMixin,
    NDCUDocPDFMixin,
    NDCUDocMetadataMixin,
):
    pass
