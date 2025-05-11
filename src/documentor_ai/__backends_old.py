import os
from typing import Tuple, Literal
from types import MappingProxyType
from pydantic import BaseModel


class BackendInfo(BaseModel):
    base_url: str
    api_key_key: str
    _api_key: str | None = None

    @property
    def api_key(self) -> str:
        if not self._api_key:
            self._api_key = os.getenv(self.api_key_key)
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str) -> None:
        self._api_key = value


# Define backend infos
openai_backend_info = BackendInfo(
    base_url = 'https://api.openai.com/v1/',
    api_key_key = 'OPENAI_API_KEY',
)

groq_backend_info = BackendInfo(
    base_url = 'https://api.groq.com/openai/v1',
    api_key_key = 'GROQ_API_KEY',
)

nvidia_nim_backend_info = BackendInfo(
    base_url = 'https://integrate.api.nvidia.com/v1',
    api_key_key = 'NVIDIA_NIM_API_KEY',
)


# Immutable dictionary of available backends
_AVAILABLE_BACKENDS = MappingProxyType({
        'groq': groq_backend_info,
        'openai': openai_backend_info,
        'nvidia-nim': nvidia_nim_backend_info,
})


def get_available_backends(
    return_type: Literal['names', 'backends', 'groq', 'openai', 'nvidia-nim'] | None = None
) -> MappingProxyType[str, BackendInfo] | Tuple[str] | Tuple[BackendInfo] | BackendInfo | None:
    """ Returns an immutable dictionary of available backends """
    global _AVAILABLE_BACKENDS

    if not return_type:
        return _AVAILABLE_BACKENDS
    
    if return_type == 'names':
        return tuple(_AVAILABLE_BACKENDS.keys())
    elif return_type == 'backends':
        return tuple(_AVAILABLE_BACKENDS.values())
    
    return _AVAILABLE_BACKENDS.get(return_type)


if __name__ == '__main__':
    import json

    def pretty_print(data: dict | list | MappingProxyType) -> None:
        print(json.dumps(data.copy(), indent=4))

    print(get_available_backends())
