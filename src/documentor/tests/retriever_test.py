from documentor.llm import Retriever

def test_retriever() -> None:
    ret = Retriever()
    print(ret.generate_multi_query('What is self-attention in DL?'))
    
