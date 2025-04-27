from documentor.chat import ChatHistoryManager

def test_chat_history() -> None:
    chm = ChatHistoryManager()
    # print(chm.list_chats())
    print(chm.get_chat_file_path('dummy_chat.json'))
