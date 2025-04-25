import os
import json
from abc import ABC, abstractmethod
from .data import DocumentData


class Document(DocumentData, ABC):
    def __init__(self, 
        fp: str, 
        cache_dir_path: str | None = None,
    ) -> None:
        DocumentData.__init__(self)

        # set cache directory path if provided
        if cache_dir_path:
            self.cache_dir_path = cache_dir_path

        # set file path
        self.file_path = fp
    
    def load_cache(self) -> None:
        _cache_data: dict = {}
        
        try:
            with open(self.cache_file_path, 'r') as _cache_file:
                _cache_data = json.load(_cache_file)
            
            # set file metadata
            self._file_name = _cache_data['metadata']['filename']
            self._file_type = _cache_data['metadata']['filetype']
            self._file_path = _cache_data['metadata']['filepath']

            # set cache metadata
            self._cache_file_path = _cache_data['cache-metadata']['cachedir']
            self._cache_dir_path = _cache_data['cache-metadata']['cachefile']
            self._cache_file_type = _cache_data['cache-metadata']['cachefiletype']

            # set file data
            self.contents = _cache_data['contents']
            self.character_chunks = _cache_data['character-chunks']
            self.token_chunks = _cache_data['token-chunks']
            self.token_ids = _cache_data['token-ids']

        except Exception as e:
            print(f"Exception from {__name__}: {e}")

    def save_cache(self, indent: int = 4) -> None:
        """Things to Cache:
            - metadata:
                - filename
                - filetype
                - filepath
            - cache paths:
                - file
                - dir
            - contents
            - character chunks
            - token chunks
            - token ids
        """
        
        _cache_data = {
            'metadata': self.metadata(),
            'cache-metadata': self.cache_metadata(),

            'contents': self.contents,
            'character-chunks': self.character_chunks,
            'token-chunks': self.token_chunks,
            'token-ids': self.token_ids
        }

        try:
            with open(self.cache_file_path, 'w') as _cache_file:
                json.dump(_cache_data, _cache_file, indent=indent)
        except Exception as e:
            print(f"Exception from {__name__}: {e}")
    
    @abstractmethod
    def load_contents(self) -> None:
        pass

    def load(self, 
        use_cache_if_exists: bool = True, 
        create_cache_if_not_exists: bool = True
    ) -> None:
        """Load document contents and do the "preprocessing".
        """

        document_loaded = False

        # Loading from cache is only possible when:
        #   - use_cache_if_exists = True
        #   - and cache file actually exists
        if use_cache_if_exists:
            if os.path.exists(self.cache_file_path):
                self.load_cache()
                document_loaded = True
        
        # Otherwise we have to load manually everything
        if not document_loaded:
            # *** LOAD EVERYTHING MANUALLY ***
            self.load_contents()
            
            # save cache if permitted
            if create_cache_if_not_exists:
                self.save_cache()
