from typing import List
from datetime import datetime as dt

from ..llm import GroqModel
from .data_models import ChatMessage, ChatMetadata


class Chat(GroqModel):
        
    def __init__(self) -> None:
        GroqModel.__init__(self)

        # Will be `True` after calling init() method
        self._chat_ready: bool = False

        self._metadata: ChatMetadata = None
        self._messages: List[ChatMessage] = None
    
    def is_empty(self) -> bool:
        return (self._messages is None) or (len(self._messages) <= 1)
    
    def is_ready(self) -> bool:
        return self._chat_ready
    
    def init(self, system_prompt: str, model_name: str | None = None) -> None:
        if model_name:
            self.model_name = model_name
        
        self._messages = [
            self.create_system_message(system_prompt)
        ]
        
        # set metadata
        self._metadata = ChatMetadata(
            created = dt.now(),
            last_accessed = dt.now(),
            model_name = self.model_name
        )

        self._chat_ready = True

    def metadata(self) -> dict[str, str] | None:
        return self._metadata if self._chat_ready else None
    
    def load_from(self, data: dict) -> None:
        self._metadata = ChatMetadata.from_data(data['metadata'])
        self._messages = data['messages']
        self._chat_ready = True
    
    def messages(self) -> List[dict[str, str]]:
        return self._messages


def test_chat() -> None:
    # cmd = ChatMetadata(
    #     created=dt.now(),
    #     last_accessed=dt.now(),
    #     model_name='llama'
    # )

    cmd = ChatMetadata.draft()

    # print(cmd.creation_datetime_str())
    print(cmd.model_dump_json())
    print(cmd.created_datetime_as_str())
