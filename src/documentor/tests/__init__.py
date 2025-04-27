from .document_test import test_document
from .pdf_doc_test import test_pdf_document
from .text_doc_test import test_text_document
from .vectordb_man_test import test_vectordb_manager
from .groq_model_test import test_groq_model
from .retriever_test import test_retriever
from .docman_test import test_document_manager
from .chat_system_test import test_chat_system
from .chat_history_test import test_chat_history

from ..utils import pretty_print
from typing import Callable, List

class TestClass:
    test_functions = [
        test_document,
        test_pdf_document,
        test_text_document,
        test_vectordb_manager,
        test_groq_model,
        test_retriever,
        test_document_manager,
        test_chat_system,
        test_chat_history
    ]

    def list_test_functions(self) -> dict[str, dict[str, Callable | int]]:
        functions = {}
        
        for i, func in enumerate(self.test_functions):
            functions[func.__name__] = {
                'function': func,
                'function_id': i
            }
        
        return functions
    
    def print_test_function_list(self) -> None:
        pretty_print(self.list_test_functions())

    def run_test_function(self, function_id: int) -> None:
        self.test_functions[function_id]()
