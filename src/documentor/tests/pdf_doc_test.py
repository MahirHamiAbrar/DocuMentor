from documentor.tests.utils import get_path
from documentor.docs.pdf import PDFDocument

def test_pdf_document() -> None:
    doc = PDFDocument(
        fp=get_path('data/microsoft-annual-report.pdf')
    )
    doc.cache_dir_path = get_path('cache')

    doc.load(
        use_cache_if_exists=True,
        create_cache_if_not_exists=True
    )

    print(doc.metadata())
    print(doc.cache_metadata())
    print(len(doc.contents))