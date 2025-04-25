from loguru import logger
from rich.progress import track
from typing import List, Callable

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter
)

from .data import DocumentData


class TextSplitter:

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

        document_data: DocumentData,

        # parameters for 'RecorsiveChartacterTextSplitter' aka 'RCTS'
        rcts_separators: List[str] | None = None,
        rcts_chunk_size: int | None = None,
        rcts_chunk_overlap: int | None = None,
        rcts_length_function: Callable | None = None,

        # parameters for 'SentenceTransformersTokenTextSplitter' aka 'STTTS'
        sttts_chunk_overlap: int | None = None,
        sttts_tokens_per_chunk: int | None = None,
        sttts_length_function: Callable | None = None
    ) -> None:
        
        self._document_data: DocumentData = document_data
        
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
    
    def split_characters_into_chunks(self) -> None:
        try:
            logger.info(
                f'Splitting Characters into chunks of ' \
                f'{self._character_splitter._chunk_size} characters ' \
                f'with {self._character_splitter._chunk_overlap} overlap.'
            )

            self._document_data.character_chunks = self._character_splitter.split_text(
                text=self._document_data.contents_as_str()
            )

        except Exception as e:
            logger.error(e)
    
    def split_chunks_into_tokens(self) -> None:
        """ Splits the document's character chunks into token chunks and assigns unique token IDs. """        
        try:
            logger.info(
                f'Splitting Tokens into chunks of ' \
                f'{self._token_splitter._chunk_size} characters ' \
                f'with {self._token_splitter._chunk_overlap} overlap.'
            )

            # tokenize chunks
            tokens = []

            for chunk in self._document_data.character_chunks:
                tokens.append(self._token_splitter.split_text(text=chunk))

            self._document_data.token_chunks = tokens

            # create token ids
            ids = []

            for i in range(1, len(self._document_data.token_chunks) + 1):
                ids.append(f"{self._document_data.file_name}-token-{i}")
                
            self._document_data.token_ids = ids

        except Exception as e:
            logger.error(e)
