from documentor.docs.text_doc import TextDocument
from documentor.tests.utils import get_path, pretty_print

def test_text_document() -> None:
    doc = TextDocument(
        fp=get_path('data/attention-is-all-you-need-paper.txt')
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
