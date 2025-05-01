import os
import json

project_dir = os.path.dirname(__file__)


def get_internal_path(*paths: str) -> str:
    global project_dir
    return os.path.join(project_dir, *paths)

def pretty_print(
    data: dict | list, 
    indent: int = 4, 
    end='\n'
) -> str:
    print(json.dumps(data, indent=indent), end=end)


def get_ui_resource_path(fp: str, must_exist: bool = True) -> str:
    path = os.path.join(project_dir, 'ui/resources', fp)
    if must_exist:
        assert os.path.exists(path), f'path: {fp} does not exist in ui/resources'
    return path

def get_ui_file_path(fname: str, must_exist: bool = False) -> str:
    return get_ui_resource_path(f'ui_files/{fname}', must_exist)

def get_ui_stylesheet_path(fname: str, must_exist: bool = False) -> str:
    return get_ui_resource_path(f'styles/{fname}', must_exist)

def get_ui_icon_path(fname: str, must_exist: bool = False) -> str:
    return get_ui_resource_path(f'icons/{fname}', must_exist)
