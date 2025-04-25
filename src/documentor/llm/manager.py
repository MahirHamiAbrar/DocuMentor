import os
from typing import List, Callable

from loguru import logger
from dotenv import load_dotenv

from groq import Groq
from groq.types import ModelListResponse

from .prompts import *

load_dotenv()

class LLMManager:
    def __init__(self) -> None:
        self._client: Groq = Groq(
            api_key = os.getenv("GROQ_API_KEY")
        )

        # stream callback function
        self._stream_callback: Callable = print

        # model to be used
        self._model_name: str = 'llama-3.3-70b-versatile'
    
    def get_model_name(self) -> str:
        return self._model_name
    
    def set_model_name(self, model_name: str) -> None:
        self._model_name = model_name
    
    def get_model_list(self) -> List[ModelListResponse]:
        return self._client.models.list()
    
    def set_stream_callback_function(self, callback_function: Callable) -> None:
        assert callable(callback_function), "Provided callback function isn't callable!"
        self._stream_callback = callback_function
    
    def _invoke_stream_callback_function(self, *args, **kwargs) -> None:
        assert callable(self._stream_callback), \
             "Provided callback function is not set or isn't callable!"
        self._stream_callback(*args, **kwargs)
    
    def create_user_query_for_multiquery(self,
        query_text: str,
        retrieved_documents: List[str]
    ) -> dict[str, str]:
        
        documents = ""
        for i, document in enumerate(retrieved_documents):
            documents += f"\n\n\tDocument #{i + 1}:\n\t\t{document}"
        
        user_query_content = (
            f"Query: {query_text}"
            "Relevant Documents:\n"
            f"{documents.strip()}"
        )
        
        return user_query_content
    
    def generate_response(self,
        system_prompt: str,
        user_query: str
    ) -> str:
        response = self._client.chat.completions.create(
            model = self._model_name,
            messages=[
                { 'role': 'system', 'content': system_prompt },
                { 'role': 'user', 'content': user_query }
            ]
        )

        return response.choices[0].message.content
    
    def generate_response_from_history(self,
        history: List[dict[str, str]],
        user_query: str
    ) -> None:
        
        history.append({
            'role': 'user', 'content': user_query
        })
        
        response = self._client.chat.completions.create(
            model = self._model_name,
            messages = history
        )
        reply_content = response.choices[0].message.content

        history.append({
            'role': 'assistant', 'content': reply_content
        })

        return reply_content
    
    def generate_multi_query(self,
        query: str
    ) -> List[str]:
        return self.generate_response(
            system_prompt=multi_query_system_prompt,
            user_query=query
        ).split('\n')
    
    def generate_response_for_retrieved_documents(self, 
        user_query: str,
        retrieved_documents: List[str]
    ) -> str:
        
        user_query_content = self.create_user_query(
            user_query,
            retrieved_documents
        )

        return self.generate_response(
            system_prompt=final_response_system_prompt,
            user_query=user_query_content
        )