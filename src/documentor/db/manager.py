from typing import List, Sequence
from loguru import logger

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from ..docs import Document
from ..utils import get_internal_path


class VectorDataBaseManager:

    def __init__(self, 
        save_location: str | None = None
    ) -> None:

        self._db_save_location = (
            save_location
            if save_location
            else get_internal_path('tests/chromadb')
        )

        # custom embedding function, loads embedding model locally
        # recommended to use a 'CUDA' enabled GPU.
        # Default 'jinja' model takes approx 4.5 GB VRAM.
        self._embedding_func: SentenceTransformerEmbeddingFunction | None = None
        
        # chromadb client
        self._chromadb_client = chromadb.PersistentClient(
            path=self._db_save_location
        )

        # chromadb collection
        self._chroma_collection: chromadb.Collection | None = None
    
    def load_embedding_model(self) -> None:
        logger.info('loading embedding model...')
        self._embedding_func = SentenceTransformerEmbeddingFunction(
            model_name='jinaai/jina-embeddings-v2-base-en'
        )
    
    def list_collections(self) -> Sequence[chromadb.Collection]:
        return self._chromadb_client.list_collections()
    
    def collection_exists(self, collection_name: str) -> bool:
        return collection_name in [
            collection.name for collection in self.list_collections()
        ]
    
    def load_existing_collection(self, collection_name: str) -> None:
        self._chroma_collection = self._chromadb_client.get_collection(
            name=collection_name,
            embedding_function=self._embedding_func
        )
    
    def create_chromadb_collection_from_document(self, document: Document, collection_name: str) -> None:
        try:
            logger.info('Creating ChromaDB Collection.')
            
            if not self._embedding_func:
                logger.critical('Embedding function not loaded!')
                return
            
            self._chroma_collection = self._chromadb_client.get_or_create_collection(
                name=collection_name,
                embedding_function=self._embedding_func,
            )

            metadatas: List[dict[str, str]] = [{
                'source': document.file_path
            }] * len(document.token_ids)
            
            self._chroma_collection.add(
                ids=document.token_ids,
                metadatas=metadatas,
                documents=document.token_chunks,
            )
        except Exception as e:
            logger.error(e)
    
    def create_chromadb_collection_from_data(self, 
        ids: List[str],
        document_contents: List[str],
        metadatas: List[str],
        collection_name: str
    ) -> None:
        try:
            logger.info('Creating ChromaDB Collection.')
            
            if not self._embedding_func:
                logger.critical('Embedding function not loaded!')
                return
            
            self._chroma_collection = self._chromadb_client.get_or_create_collection(
                name=collection_name,
                embedding_function=self._embedding_func,
            )
            
            self._chroma_collection.add(
                ids=ids,
                metadatas=metadatas,
                documents=document_contents,
            )
        except Exception as e:
            logger.error(e)

    def retrieve_documents(self,
        query_texts: List[str],
        n_results: int = 5,
        include: List[str] = ['documents', 'embeddings', 'metadatas']
    ) -> List[List[str]] | None:
        
        results = self._chroma_collection.query(
            query_texts=query_texts,
            n_results=n_results,
            include=include
        )

        retrieved_documents = results['documents']

        unique_docs = set([
            doc
            for docs in retrieved_documents
            for doc in docs
        ])

        return list(unique_docs)
