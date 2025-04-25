from documentor.db import VectorDataBaseManager
from documentor.docs.text_doc import TextDocument
from documentor.utils import get_internal_path


def test_vectordb_manager() -> None:
    doc = TextDocument(
        fp=get_internal_path('tests/data/attention-is-all-you-need-paper.txt'),
        cache_dir_path=get_internal_path('tests/cache')
    )
    doc.load()
    
    dbman = VectorDataBaseManager(
        collection_name='microsoft-collection'
    )
    dbman.load_embedding_model()
    dbman.create_chromadb_collection(doc)

    print("Retrieved Documents = " + dbman.retrieve_documents(
        # ['what is the goal of reducing sequential computation?'],
        ['Tell me about the model architecture.']
    ))
