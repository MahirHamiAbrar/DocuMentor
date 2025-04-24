import os
from loguru import logger
from typing import List


class Document:
    def __init__(self) -> None:
        self._file_path: str = ''
        self._file_name: str = ''
        self._file_type: str = ''

        self._cache_file_path: str = ''
        self._cache_dir_path: str = ''

        self._contents: List[str] = []
        self._character_chunks: List[str] = []
        self._token_chunks: List[str] = []
        self._token_ids: List[str] = []

        # set default cache directory
        self.cache_dir_path = './outputs'
    
    def metadata(self) -> dict[str, str]:
        return {
            'filename': self.file_name,
            'filetype': self.file_type,
            'filepath': self.file_path
        }

    @property
    def file_path(self) -> str:
        return self.file_path
    
    @file_path.setter
    def file_path(self, fp: str) -> None:
        assert os.path.exists(fp), f"File: {fp} does not exist."
        
        self._file_path = fp
        self._file_name, self._file_type = os.path.splitext(os.path.basename(fp))
        self._cache_file_path = os.path.join(self._cache_dir_path, self._file_name)

        if not os.path.exists(self._cache_dir_path):
            logger.warning(f'Provided cache directory "{self._cache_dir_path}" does not exist. Creating it now.')
            os.mkdir(self._cache_dir_path)
    
    @property
    def file_name(self) -> None:
        return self._file_name
    
    @file_name.setter
    def file_name(self, value: str) -> None:
        self._file_name = value
    
    @property
    def file_type(self) -> None:
        return self._file_type
    
    @file_type.setter
    def file_type(self, value: str) -> None:
        self._file_type = value
        
    @property
    def cache_dir_path(self) -> None:
        return self._cache_dir_path
    
    @cache_dir_path.setter
    def cache_dir_path(self, path: str) -> None:
        assert os.path.exists(path) and not os.path.isdir(path), \
            f"path: `{path}` exists but is not a directory!"

        if not os.path.exists(path):
            os.mkdir(path)

        self._cache_dir_path = path
    
    @property
    def contents(self) -> List[str]:
        return self._contents
    
    @contents.setter
    def contents(self, data: List[str]) -> None:
        # self._contents = data.copy()
        self._contents = data
    
    def contents_as_str(self, seperator: str = '\n\n') -> str:
        return seperator.join(self.contents)
    
    @property
    def character_chunks(self) -> List[str]:
        return self._character_chunks
    
    @character_chunks.setter
    def character_chunks(self, data: List[str]) -> None:
        # self._character_chunks = data.copy()
        self._character_chunks = data
    
    @property
    def token_chunks(self) -> List[str]:
        return self._token_chunks
    
    @token_chunks.setter
    def token_chunks(self, data: List[str]) -> None:
        # self._token_chunks = data.copy()
        self._token_chunks = data
    
    @property
    def token_ids(self) -> List[str]:
        return self._token_ids
    
    @token_ids.setter
    def token_ids(self, data: List[str]) -> None:
        # self._token_ids = data.copy()
        self._token_ids = data
