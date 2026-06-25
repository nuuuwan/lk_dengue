from dengue.ndcu_doc.NDCUDocBase import NDCUDocBase
from dengue.ndcu_doc.NDCUDocBuilderMixin import NDCUDocBuilderMixin
from dengue.ndcu_doc.NDCUDocCustomDataMixin import NDCUDocCustomDataMixin
from dengue.ndcu_doc.NDCUDocLoaderMixin import NDCUDocLoaderMixin
from dengue.ndcu_doc.NDCUDocMetadataMixin import NDCUDocMetadataMixin
from dengue.ndcu_doc.NDCUDocPDFMixin import NDCUDocPDFMixin
from dengue.ndcu_doc.NDCUDocRawTablesMixin import NDCUDocRawTablesMixin
from dengue.ndcu_doc.NDCUDocReadMeMixin import NDCUDocReadMeMixin


class NDCUDoc(
    NDCUDocBase,
    #
    NDCUDocLoaderMixin,
    NDCUDocBuilderMixin,
    #
    NDCUDocMetadataMixin,
    NDCUDocPDFMixin,
    NDCUDocRawTablesMixin,
    NDCUDocCustomDataMixin,
    #
    NDCUDocReadMeMixin,
):
    pass
