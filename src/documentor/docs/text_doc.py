from loguru import logger
from .document import Document

# TODO: Add support for docx files


class TextDocument(Document):
    def __init__(self, fp: str, cache_dir_path: str | None = None) -> None:
        Document.__init__(self, fp, cache_dir_path)
    
    def load_contents(self) -> None:
        logger.info('Extracting text from the TXT document...')

        try:
            with open(self.file_path, 'r') as _text_file:
                self.contents = _text_file.read().strip().split('\n')
        except Exception as e:
            logger.error(f"{e}")
