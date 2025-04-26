from ..chat import ChatSystem
from documentor.utils import get_internal_path


def test_chat_system() -> None:
    cs = ChatSystem(
        cache_dir=get_internal_path('tests/cache'),
        vector_store_save_location=get_internal_path('tests/chromadb')
    )

    # add dcuments
    cs.add_file(get_internal_path('tests/data/microsoft-annual-report.pdf'))
    cs.add_file(get_internal_path('tests/data/attention-is-all-you-need-paper.txt'))

    # load all documents
    cs.load_all_documents()
    print(f"Total Documents: {cs.document_count()}")

    # load embedding model
    cs.load_embedding_model()
    # save/load data to/from vector storage
    cs.save_to_vector_store('attention-paper_and_microsoft-tech-report')

    cs.invoke(
        user_query='Tell me about the "OPERATING SEGMENTS"'
    )
