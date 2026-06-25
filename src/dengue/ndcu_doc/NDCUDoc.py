from dengue.ndcu_doc.NDCUDocBase import NDCUDocBase
from dengue.ndcu_doc.NDCUDocBuilderMixin import NDCUDocBuilderMixin
from dengue.ndcu_doc.NDCUDocLoaderMixin import NDCUDocLoaderMixin
from dengue.ndcu_doc.NDCUDocMetadataMixin import NDCUDocMetadataMixin
from dengue.ndcu_doc.NDCUDocPDFMixin import NDCUDocPDFMixin
from dengue.ndcu_doc.NDCUDocTablesMixin import NDCUDocTablesMixin


class NDCUDoc(
    NDCUDocBase,
    #
    NDCUDocLoaderMixin,
    NDCUDocBuilderMixin,
    #
    NDCUDocMetadataMixin,
    NDCUDocPDFMixin,
    NDCUDocTablesMixin,
):
    pass
