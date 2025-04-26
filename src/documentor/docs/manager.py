import os

from typing import List
from loguru import logger

from .document import Document
from .pdf_doc import PDFDocument
from .text_doc import TextDocument
from ..db import VectorDataBaseManager

class DocumentManager(VectorDataBaseManager):

    supported_file_formats: List[str] = ['pdf', 'txt']

    def __init__(self,
        cache_dir: str | None = None,
        vector_store_save_location: str | None = None
    ) -> None:
        VectorDataBaseManager.__init__(
            self,
            save_location=vector_store_save_location
        )
        
        self._cache_dir: str = cache_dir
        self._documents: List[Document] = []

    def documents(self) -> List[Document]:
        return self._documents
    
    def document_count(self) -> int:
        return len(self._documents)

    def add_file(self, fp: str) -> int:
        filetype = os.path.splitext(fp)[1][1:]
        
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
        logger.info("loading all documents...")
        
        for document in self._documents:
            document.load(
                use_cache_if_exists=use_cache_if_exists,
                create_cache_if_not_exists=create_cache_if_not_exists
            )
    
    def save_to_vector_store(self, 
        collection_name: str,
        skip_if_collection_exists: bool = True
    ) -> None:
        
        if skip_if_collection_exists:
            if self.collection_exists(collection_name):
                logger.warning('Collection already exists, so loading the existing collection.')
                self.load_existing_collection(collection_name)
                return

        ids = []
        documents = []
        metadatas = []

        for document in self._documents:
            ids.extend(document.token_ids)
            documents.extend(document.token_chunks)
            metadatas.extend([
                { 'source': document.file_path }
            ] * len(document.token_ids))
        
        self.create_chromadb_collection_from_data(
            ids, documents, metadatas, collection_name
        )
