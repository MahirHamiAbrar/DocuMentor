from ..docs import DocumentManager
from ..db import VectorDataBaseManager
from ..llm import Retriever, GroqModel
from .chat_history import ChatHistoryManager


class ChatSystem(DocumentManager):
    def __init__(self) -> None:
        DocumentManager.__init__(self)
        
        self._vector_dbman: VectorDataBaseManager | None = None
        self._retriever: Retriever = Retriever(self._vector_dbman)
        self._llm: GroqModel = GroqModel()
        self._chat_history: ChatHistoryManager = ChatHistoryManager()
    
    # def 
