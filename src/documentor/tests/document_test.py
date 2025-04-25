import json
from documentor.docs import DocumentData
from documentor.utils import get_internal_path


def test_document() -> None:

    # Create a Document() object
    doc = DocumentData()

    # Set document file path
    doc.file_path = get_internal_path('tests/data/microsoft-annual-report.pdf')
    doc.cache_dir_path = get_internal_path('tests/cache')

    # Print Document metadata
    print(f"Metadata = {json.dumps(doc.metadata(), indent=4)}")

    # ###### CACHE METADATA TEST ###### #
    # Print Cache Metadata
    print(f"CacheMetadata = {json.dumps(doc.cache_metadata(), indent=4)}")

    # change cache directory and the cache-filepath automatically changes
    doc.cache_dir_path = get_internal_path('cache2')
    print(f"CacheMetadata = {json.dumps(doc.cache_metadata(), indent=4)}")
    
    # change the cache filepath and the filetype also changes
    doc.cache_file_path = get_internal_path('cache/cache_file.csv')
    print(f"CacheMetadata = {json.dumps(doc.cache_metadata(), indent=4)}")\
    
    # THOUGHT: Will it be a wise decision to change the directory too, when the filepath changes? (sync)
