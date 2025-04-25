import os
import json

project_dir = os.path.dirname(__file__)

def get_path(*paths: str) -> str:
    global project_dir
    return os.path.join(project_dir, *paths)

def pretty_print(
    data: dict | list, 
    indent: int = 4, 
    end='\n'
) -> str:
    print(json.dumps(data, indent=indent), end=end)
