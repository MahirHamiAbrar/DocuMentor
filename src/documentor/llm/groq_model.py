import os
from typing import List, Callable

from loguru import logger
from dotenv import load_dotenv

from ..chat.data_models import ChatMessage

from groq import Groq
from groq.types import Model
from groq.resources.chat.completions import ChatCompletion

load_dotenv()


class GroqModel:
    def __init__(self) -> None:
        self._client: Groq = Groq(
            api_key = os.getenv("GROQ_API_KEY")
        )

        # stream callback function
        self._stream_callback: Callable = print

        # model to be used
        self._model_name: str = 'llama-3.3-70b-versatile'
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    @model_name.setter
    def model_name(self, name: str) -> None:
        assert self.model_valid(name), 'Invalid Model!'
        self._model_name = name
    
    @property
    def stream_callback_function(self) -> Callable:
        return self._stream_callback
    
    @stream_callback_function.setter
    def stream_callback_function(self, func: Callable) -> None:
        assert callable(func), 'Provided function is not callable!'
        self._stream_callback = func
    
    def get_model_name(self) -> str:
        return self._model_name
    
    def set_model_name(self, model_name: str) -> None:
        self._model_name = model_name
    
    def get_model_list(self) -> List[Model]:
        return self._client.models.list().data
    
    def model_valid(self, model_name: str) -> bool:
        for model in self.get_model_list():
            if model_name == model.id:
                return True
        return False
    
    def create_system_message(self, msg: str) -> ChatMessage:
        return ChatMessage(
            role = 'system',
            content = msg
        )
    
    def create_user_message(self, msg: str) -> ChatMessage:
        return ChatMessage(
            role = 'user',
            content = msg
        )
    
    def create_assistant_message(self, msg: str) -> ChatMessage:
        return ChatMessage(
            role = 'assistant',
            content = msg
        )
    
    def generate_response(self,
        messages: List[ChatMessage],
        stream: bool = False
    ) -> str:
        response: ChatCompletion = self._client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            stream=stream,
        )

        response_text = ''

        if stream:
            for chunk in response:
                chunk_text = chunk.choices[0].delta.content
                if chunk_text:
                    self.stream_callback_function(chunk_text)
                    response_text += chunk_text
        else:
            response_text = response.choices[0].message.content

        return response_text
