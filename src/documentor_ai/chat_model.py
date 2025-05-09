import os

from openai import OpenAI
from dotenv import load_dotenv

# load all environment variables
load_dotenv()


class ChatModel(OpenAI):
    def __init__(self, *, api_key = None, organization = None, project = None, base_url = None, websocket_base_url = None, timeout = ..., max_retries = ..., default_headers = None, default_query = None, http_client = None, _strict_response_validation = False):
        super().__init__(api_key=api_key, organization=organization, project=project, base_url=base_url, websocket_base_url=websocket_base_url, timeout=timeout, max_retries=max_retries, default_headers=default_headers, default_query=default_query, http_client=http_client, _strict_response_validation=_strict_response_validation)
