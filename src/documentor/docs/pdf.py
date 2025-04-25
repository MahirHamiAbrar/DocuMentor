from loguru import logger
from pypdf import PdfReader

from .document import Document


class PDFDocument(Document):
    def __init__(self, fp: str, cache_dir_path: str | None = None) -> None:
        Document.__init__(self, fp, cache_dir_path)
    
    def load_contents(self) -> None:
        logger.info('Extracting text from the PDF document...')

        texts = []
        reader = PdfReader(self._file_path)

        # for page in track(reader.pages, description="Extracting text from PDF"):
        for page in reader.pages:
            texts.append(page.extract_text().strip())
        
        self.contents = texts
