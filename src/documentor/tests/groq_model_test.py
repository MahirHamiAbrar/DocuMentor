from documentor.llm import GroqModel

def test_groq_model() -> None:
    gm = GroqModel()

    messages = [
        gm.create_system_message('You are a helpful assistant.'),
        gm.create_user_message('What is RAG (Retrieval Augmented Generation) in short?')
    ]

    resp = gm.generate_response(messages, stream=True)
    print(resp)