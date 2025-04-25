from documentor.docs import TextDocument
from documentor.utils import get_internal_path, pretty_print

def test_text_document() -> None:
    doc = TextDocument(
        fp=get_internal_path('tests/data/attention-is-all-you-need-paper.txt')
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
