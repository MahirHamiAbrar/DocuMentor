from documentor.docs import DocumentManager
from documentor.utils import get_internal_path

def test_document_manager() -> None:
    docman = DocumentManager(
        cache_dir=get_internal_path('tests/cache'),
        vector_store_save_location=get_internal_path('tests/chromadb')
    )

    # PDF Document
    docman.add_file(get_internal_path('tests/data/microsoft-annual-report.pdf'))
    # Text Document
    docman.add_file(get_internal_path('tests/data/attention-is-all-you-need-paper.txt'))
    
    docman.load_all_documents()

    print(f"Total Documents: {docman.document_count()}")

    docman.load_embedding_model()
    docman.save_to_vector_store('attention-paper_and_microsoft-tech-report')
