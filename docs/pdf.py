import os
import json

from loguru import logger
from pypdf import PdfReader

from .document import Document


class PDFDocument(Document):

    def __init__(self, fp: str, cache_dir_path: str | None = None) -> None:
        Document.__init__(self)

        # set cache directory path if provided
        if cache_dir_path:
            self.cache_dir_path = cache_dir_path

        # set file path
        self.file_path = fp
    
    def extract_texts(self) -> None:
        logger.info('Extracting text from the PDF document...')

        texts = []
        reader = PdfReader(self._file_path)

        # for page in track(reader.pages, description="Extracting text from PDF"):
        for page in reader.pages:
            texts.append(page.extract_text().strip())
        
        self.contents = texts.copy()
    
    def load_cached_contents(self) -> str:
        logger.info('Loading from the cached file.')

        contents = []
        with open(self._cache_file_path, 'r') as _json_file:
            contents = json.load(_json_file)
        return contents
    
    def save_content_cache(self, indent: int = 4) -> None:
        logger.info('Saving content cache.')

        with open(self._cache_file_path, 'w') as _json_file:
            json.dump(self._contents, _json_file, indent=indent)
        
    def load(self, force_reload: bool = False) -> None:
        if len(self.contents_as_str()) > 0 and not force_reload:
            logger.info("Document is already loaded and 'force_reload' not enabled. Skipping...")
            return
        
        # Extract texts form the PDF Document if:
        #   - 'force_reload' is enabled
        #   - Or, file is not already cached (which means you have to load the file anyway)
        if force_reload or not os.path.exists(self._cache_file_path):
            self._contents = self.extract_texts()   # Extract the texts
            self.save_content_cache()               # Cache the file
        
        # Otherwise, load from the cache (faster than extracting from the PDF)
        else:
            logger.info('Cache exists.')
            self._contents = self.load_cached_contents()
