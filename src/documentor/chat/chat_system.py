from typing import List
from loguru import logger

from ..docs import DocumentManager
from ..llm import Retriever, GroqModel
# from .chat_history import ChatHistoryManager


# class ChatSystem(DocumentManager, ChatHistoryManager):
class ChatSystem(DocumentManager):
    def __init__(self,
        cache_dir: str | None = None,
        vector_store_save_location: str | None = None
    ) -> None:
        
        DocumentManager.__init__(self,
            cache_dir=cache_dir,
            vector_store_save_location=vector_store_save_location
        )

        # ChatHistoryManager.__init__(self)

        self._llm = GroqModel()
        self._retriever: Retriever = Retriever()
    
    def invoke(self,
        user_query: str,
        n_multi_query: int = 5,
        n_retrieved_documents: int = 5,
        retrieved_documents_include: List[str] = ['documents', 'embeddings', 'metadatas']
    ) -> None:
        
        # generate multiple queries for document retrieval
        logger.info('generate multiple queries for document retrieval')
        multi_query = self._retriever.generate_multi_query(
            query=user_query,
            n_queries=n_multi_query
        )

        # print(f"{multi_query = }")

        # retrieve documents from vector database
        logger.info('retrieve documents from vector database')
        retrieved_documents = self.retrieve_documents(
            query_texts=multi_query,
            n_results = n_retrieved_documents,
            include = retrieved_documents_include
        )
        # print(f"{retrieved_documents = }")

        # create user message (for LLM) based on the retrieved documents
        # user_message = self._retriever.create_user_message_from_retrieved_documents(
            # query_text=user_query,
            # retrieved_documents=retrieved_documents
        # )

        logger.info('generating response')
        response = self._retriever.generate_response_for_retrieved_documents(
            user_query=user_query,
            retrieved_documents=retrieved_documents,
            stream=None
        )

        print(f"{response = }")
