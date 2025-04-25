from documentor.docs import PDFDocument
from documentor.utils import get_internal_path, pretty_print

def test_pdf_document() -> None:
    doc = PDFDocument(
        fp=get_internal_path('tests/data/microsoft-annual-report.pdf')
    )
    doc.cache_dir_path = get_internal_path('tests/cache')

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
