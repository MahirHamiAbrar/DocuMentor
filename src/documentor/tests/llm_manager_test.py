from documentor.llm import LLMManager

def test_llm_manager() -> None:
    man = LLMManager()
    print(man.generate_multi_query('What is self attention?'))
