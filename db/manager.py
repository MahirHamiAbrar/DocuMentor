import sys, time
from loguru import logger

# setup logger
try:
    logger.remove(0)
except Exception as e:
    print(f"Error: {e}")

logfile_name = f'log-{int(time.time())}.txt'
with open(logfile_name, 'w') as logfile:
    logfile.write('=' * 10 + 'LOG FILE GENERATED' + '=' * 10)

logfile = open(logfile_name, 'a')
logger.add(logfile, level="TRACE")

from rich.progress import track
from typing import List, Callable

import chromadb
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter
)

from document_manager import DocumentManager
from embedding_function import CustomEmbeddingFunction


class VectorDataBaseManager:

    # 'RecorsiveChartacterTextSplitter' aka 'RCTS' default config
    RCTS_SEPARATORS: List[str] = ['\n\n', '\n', '. ', ' ', '']
    RCTS_CHUNK_SIZE: int = 1024
    RCTS_CHUNK_OVERLAP: int = 128
    RCTS_LENGTH_FUNCTION: Callable = len

    # 'SentenceTransformersTokenTextSplitter' aka 'STTTS' default config
    STTTS_CHUNK_OVERLAP: int = 64
    STTTS_TOKENS_PER_CHUNK: int = 256
    STTTS_LENGTH_FUNCTION: Callable = len

    def __init__(
        self,
        document_manager: DocumentManager,

        # parameters for 'RecorsiveChartacterTextSplitter' aka 'RCTS'
        rcts_separators: List[str] | None = None,
        rcts_chunk_size: int | None = None,
        rcts_chunk_overlap: int | None = None,
        rcts_length_function: Callable | None = None,

        # parameters for 'SentenceTransformersTokenTextSplitter' aka 'STTTS'
        sttts_chunk_overlap: int | None = None,
        sttts_tokens_per_chunk: int | None = None,
        sttts_length_function: Callable | None = None,

        collection_name: str = 'Chatbot-Chroma-Collection'
    ) -> None:
        
        self._docman: DocumentManager = document_manager

        # embedding function 
        # loading takes time, so to prevent GUI application freezing,
        # `load_embedding_model()` method must be called after creating
        # an instance of `ChatBot()` class.
        self._embedding_func: CustomEmbeddingFunction | None = None
        
        # chromadb client
        self._chromadb_client = chromadb.Client()

        # chromadb collection
        self._chroma_collection: chromadb.Collection = self._chromadb_client.create_collection(
            name=collection_name,
            embedding_function=self._embedding_func,
        )

        # character splitter
        self._character_splitter = RecursiveCharacterTextSplitter(
            separators = rcts_separators or self.RCTS_SEPARATORS,
            chunk_size = rcts_chunk_size or self.RCTS_CHUNK_SIZE,
            chunk_overlap = rcts_chunk_overlap or self.RCTS_CHUNK_OVERLAP,
            length_function = rcts_length_function or self.RCTS_LENGTH_FUNCTION,
        )

        # token splitter
        self._token_splitter = SentenceTransformersTokenTextSplitter(
            chunk_overlap = sttts_chunk_overlap or self.STTTS_CHUNK_OVERLAP,
            tokens_per_chunk = sttts_tokens_per_chunk or self.STTTS_TOKENS_PER_CHUNK,
            length_function = sttts_length_function or self.STTTS_LENGTH_FUNCTION,
        )

    def load_embedding_model(self) -> None:
        self._embedding_func = CustomEmbeddingFunction()
    
    def split_characters_into_chunks(self) -> None:
        try:
            logger.info(
                f'Splitting Characters into chunks of ' \
                f'{self._character_splitter._chunk_size} characters ' \
                f'with {self._character_splitter._chunk_overlap} overlap.'
            )

            for document in track(
                self._docman.document_collection().values(),
                description='Splitting Characters into Chunks:'
            ):
                chunks = self._character_splitter.split_text(
                    document.contents_as_str()
                )
                document.set_character_chunks(chunks)
        except Exception as e:
            logger.error(e)
    
    def split_tokens(self) -> None:
        try:
            logger.info(
                f'Splitting Tokens into chunks of ' \
                f'{self._token_splitter._chunk_size} characters ' \
                f'with {self._token_splitter._chunk_overlap} overlap.'
            )

            for document in track(
                self._docman.document_collection().values(),
                description='Splitting Characters into Tokens:'
            ):
                chunks = self._token_splitter.split_text(
                    document.contents_as_str()
                )
                document.set_token_chunks(chunks)
                document.set_token_ids([
                    str(i) for i in range(0, len(document.token_chunks()))
                ])
        except Exception as e:
            logger.error(e)
    
    def create_chromadb_collection(self) -> None:
        try:
            logger.info('Creating ChromaDB Collection.')

            ids: List[str] = []
            documents: List[str] = []
            metadatas: List[dict[str, str]] = []

            for document in track(
                self._docman.document_collection().values(),
                description='Creating ChromaDB Collection:'
            ):
                documents.append(document.token_chunks())
                metadatas.append({
                    'source': document.file_path()
                })
                ids.append(document.token_ids())
            
            self._chroma_collection.add(
                ids=ids,
                metadatas=metadatas,
                documents=documents,
            )
        except Exception as e:
            logger.error(e)
    
    def preprocess(
        self, 
        progress_callback_function: Callable | None = None
    ) -> None:
        # load the embedding function if not already loaded
        if not self._embedding_func:
            progress_callback_function(status='Loading Embedding Model')
            self.load_embedding_model()
        
        # 1. Do character splitting
        progress_callback_function(status='Splitting Characters into Chunks')
        self.split_characters_into_chunks()

        # 2. Split token texts
        progress_callback_function(status='Splitting Characters into Token Texts')
        self.split_tokens()

        # 3. Create collection in ChromaDB
        progress_callback_function(status='Creating ChromaDB Collection')
        self.create_chromadb_collection()
    
    def retrieve_documents(
        self,
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


def test_dbman() -> None:
    from document_manager import DocumentManager

    docman = DocumentManager()
    docman.add_pdf_file(
        file_path='./data/microsoft-annual-report.pdf',
        load_document=True
    )

    def progress_callback_function(status: str) -> None:
        print(f'[ dbman-status ]: {status}')

    dbman = VectorDataBaseManager(document_manager=docman)
    # dbman.preprocess(progress_callback_function)


if __name__ == '__main__':
    test_dbman()
    logfile.close()
