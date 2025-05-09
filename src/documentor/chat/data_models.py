from pydantic import BaseModel
from datetime import datetime as dt


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatMetadata(BaseModel):
    created: dt
    last_accessed: dt
    model_name: str
    datetime_format: str = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def from_data(data: dict) -> 'ChatMetadata':
        return ChatMetadata(
            created = data['created'],
            last_accessed = data['last_accessed'],
            model_name = data['model_name'],
            datetime_format = data['datetime_format']
        )
    
    @staticmethod
    def draft() -> 'ChatMetadata':
        """ Returns an instance of `ChatMetadata` class with default `None` value variables. """
        return ChatMetadata(
            created = dt.now(),
            last_accessed = dt.now(),
            model_name = ''
        )

    def created_datetime_as_str(self) -> str:
        return dt.strftime(self.created, self.datetime_format)
    
    def last_accessed_datetime_as_str(self) -> str:
        return dt.strftime(self.last_accessed, self.datetime_format)
