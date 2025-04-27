from documentor.tests import TestClass

def main() -> None:
    tc = TestClass()
    # print(tc.list_test_functions())

    # test_chat_system: 7
    # test_chat_history: 8
    tc.run_test_function(8)
