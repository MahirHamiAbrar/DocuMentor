import os
from typing import Tuple

project_dir = os.path.dirname(__file__)

def get_path(*paths: str) -> str:
    global project_dir
    return os.path.join(project_dir, *paths)
