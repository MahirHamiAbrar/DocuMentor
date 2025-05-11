from typing import Literal, Optional
from documentor_ai._types import Message, Messages


class ChatMessages:
    def __init__(self,
        system_prompt: str | None = None
    ) -> None:
        
        self._messages: Messages = []

        if system_prompt:
            self.add_system_message(system_prompt)
    
    def messages(self) -> Messages:
        return self._messages
    
    def message_count(self, 
        key: Optional[Literal['user', 'assistant', 'tool']] = None
    ) -> int:
        if not key:
            return len(self._messages)
        
        return sum(1 for msg in self._messages if msg['role'] == key)
    
    def is_empty(self) -> bool:
        return len(self._messages) == 0
    
    def clear(self) -> None:
        self._messages.clear()
    
    def add_message(self,
        role: str,
        content: str
    ) -> Message:
        msg = { 'role': role, 'content': content }
        self._messages.append(msg)
        return msg
    
    def add_system_message(self, content: str) -> Message:
        return self.add_message('system', content)
    
    def add_user_message(self, content: str) -> Message:
        return self.add_message('user', content)
    
    def add_assistant_message(self, content: str) -> Message:
        return self.add_message('assistant', content)
    
    def add_tool_message(self, content: str) -> Message:
        return self.add_message('tool', content)


if __name__ == '__main__':
    cm = ChatMessages()
    for i in range(10): cm.add_user_message(f'um {i + 1}')
    for i in range(10): cm.add_assistant_message(f'am {i + 1}')
    print(cm.message_count())
