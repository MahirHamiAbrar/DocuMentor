from documentor.docs.pdf import PDFDocument
from documentor.tests.utils import get_path, pretty_print

def test_pdf_document() -> None:
    doc = PDFDocument(
        fp=get_path('data/microsoft-annual-report.pdf')
    )
    doc.cache_dir_path = get_path('cache')

    doc.load(
        use_cache_if_exists=True,
        create_cache_if_not_exists=True
    )

    pretty_print(doc.metadata())
    pretty_print(doc.cache_metadata())
    print(
        f" {len(doc.contents) = }\n",
        f"{len(doc.token_chunks) = }\n",
        f"{len(doc.token_ids) = }"
    )
