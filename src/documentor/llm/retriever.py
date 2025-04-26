from typing import List
from loguru import logger

from .prompts import *
from .groq_model import GroqModel


class Retriever(GroqModel):
    def __init__(self) -> None:
        GroqModel.__init__(self)
    
    def create_user_message_from_retrieved_documents(self,
        query_text: str,
        retrieved_documents: List[str]
    ) -> dict[str, str]:
        
        documents = ""
        for i, document in enumerate(retrieved_documents):
            documents += f"\n\n\tDocument #{i + 1}:\n\t\t{document}"
        
        user_query_content = f"Query: {query_text}" \
            "Relevant Documents:\n" \
            f"{documents.strip()}"
        
        return self.create_user_message(user_query_content)
    
    def generate_multi_query(self,
        query: str,
        n_queries: int = 5,
        stream: bool = False
    ) -> List[str]:
        return self.generate_response(
            messages=[
                self.create_system_message(multi_query_system_prompt.format(n_queries)),
                self.create_user_message(query)
            ],
            stream=stream
        ).split('\n')
    
    def generate_response_for_retrieved_documents(self, 
        user_query: str,
        retrieved_documents: List[str],
        stream: bool = False
    ) -> str:
        
        return self.generate_response(
            messages=[
                self.create_system_message(final_response_system_prompt),
                self.create_user_message_from_retrieved_documents(
                    user_query,
                    retrieved_documents
                )
            ],
            stream=stream
        )
