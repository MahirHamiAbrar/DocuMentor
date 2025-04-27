import os
import json

from typing import List
from loguru import logger

from ..utils import get_internal_path

class ChatHistoryManager:
    def __init__(self, 
        history_save_dir: str | None = None
    ) -> None:
        
        self.history_save_dir = (
            history_save_dir
            if history_save_dir
            else get_internal_path('tests/chat_history')
        )

        self._current_chat: dict = {}
    
    @property
    def history_save_dir(self) -> str:
        return self._history_save_dir
    
    @history_save_dir.setter
    def history_save_dir(self, fp: str) -> None:
        os.makedirs(fp, exist_ok=True)
        self._history_save_dir = fp
    
    def list_chats(self) -> List[str]:
        return os.listdir(self.history_save_dir)
    
    def get_chat_file_path(self,
        chat_filename: str, 
        must_exist: bool = True
    ) -> str:
        fp = os.path.join(self.history_save_dir, chat_filename)
        if must_exist:
            assert os.path.exists(fp), f'Chat file: `{chat_filename}` does not exist!'
        return fp
    
    def load_chat(self, chat_filename: str) -> dict:
        try:
            with open(self.get_chat_file_path(chat_filename), 'r') as chat_file:
                self._current_chat = json.load(chat_file)
        except Exception as e:
            logger.error(f"{e}")
    
    def save_current_chat(self,
        chat_filename: str, 
        indent: int = 4
    ) -> None:
        try:
            chat_fp = self.get_chat_file_path(chat_filename, must_exist=False)
            with open(chat_fp, 'w') as chat_file:
                json.dump(self._current_chat, chat_file, indent=indent)
        except Exception as e:
            logger.error(f"{e}")
    
    def current_chat_history(self) -> dict:
        return self._current_chat
    
    def clear_current_chat_history(self) -> None:
        self._current_chat.clear()

