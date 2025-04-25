import os

from typing import List
from loguru import logger

from .document import Document
from .pdf_doc import PDFDocument
from .text_doc import TextDocument


class DocumentManager:

    supported_file_formats: List[str] = ['pdf', 'txt']

    def __init__(self, cache_dir: str | None = None) -> None:
        self._cache_dir: str = cache_dir
        self._documents: List[Document] = []

    def add_file(self, fp: str) -> int:
        filetype = os.path.splitext(fp)[0][1:]
        
        assert filetype in self.supported_file_formats, \
            f"Provided filetype is not supported yet. Supported file formats are: {self.supported_file_formats}"
        
        if filetype == 'pdf':
            document = PDFDocument(fp, self._cache_dir)
        elif filetype == 'txt':
            document = TextDocument(fp, self._cache_dir)
        
        self._documents.append(document)
        
        # the document-id that will later be used to remove it form the list
        return len(self._documents) - 1
    
    def remove_file(self, file_id: int) -> None:
        assert len(self._documents) > 0 and file_id >= 0 and file_id < len(self._documents), \
               "Invalid ID provided!"
        
        self._documents.pop(file_id)

        # TODO: also remove it from the vector database!
    
    def load_all_documents(self, 
        use_cache_if_exists: bool = True, 
        create_cache_if_not_exists: bool = True
    ) -> None:
        
        for document in self._documents:
            document.load(
                use_cache_if_exists=use_cache_if_exists,
                create_cache_if_not_exists=create_cache_if_not_exists
            )
