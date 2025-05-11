import os
from types import MappingProxyType
from typing import Tuple, Literal, Optional, Dict, Union
from pydantic import BaseModel


class BackendInfo(BaseModel):
    """Configuration for an AI backend service."""
    base_url: str
    api_key_key: str
    default_model_name: str
    _api_key: str | None = None

    @property
    def api_key(self) -> str:
        """Get the API key, loading it from environment variables if not cached."""
        if not self._api_key:
            self._api_key = os.getenv(self.api_key_key)
            if not self._api_key:
                raise ValueError(f"API key not found in environment variable: {self.api_key_key}")
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str) -> None:
        """Set the API key manually."""
        if not value:
            raise ValueError("API key cannot be empty")
        self._api_key = value

    def __str__(self) -> str:
        """String representation of the backend info."""
        return (
            f"{self.__class__.__name__}"
            f"(base_url={self.base_url}, "
            f"api_key_key={self.api_key_key}, "
            f"default_model_name={self.default_model_name})"
        )


# Define backend configurations
BACKEND_CONFIGS: Dict[str, Dict[str, str]] = {
    'openai': {
        'base_url': 'https://api.openai.com/v1/',
        'api_key_key': 'OPENAI_API_KEY',
        "default_model_name": 'gpt-4o'
    },
    'groq': {
        'base_url': 'https://api.groq.com/openai/v1',
        'api_key_key': 'GROQ_API_KEY',
        "default_model_name": 'llama-3.3-70b-versatile'
    },
    'nvidia-nim': {
        'base_url': 'https://integrate.api.nvidia.com/v1',
        'api_key_key': 'NVIDIA_NIM_API_KEY',
        "default_model_name": 'nvidia/llama-3.3-nemotron-super-49b-v1'
    },
}


# Create immutable dictionary of available backends
_AVAILABLE_BACKENDS = MappingProxyType({
    name: BackendInfo(**config)
    for name, config in BACKEND_CONFIGS.items()
})


def get_available_backends(
    return_type: Optional[Literal['names', 'backends', 'groq', 'openai', 'nvidia-nim']] = None
) -> Union[MappingProxyType[str, BackendInfo] | Tuple[str] | Tuple[BackendInfo] | BackendInfo]:
    """
    Get available backend configurations.
    
    Args:
        return_type: Type of return value:
            - None: Returns all backends
            - 'names': Returns backend names
            - 'backends': Returns backend objects
            - Specific backend name: Returns that backend
    
    Returns:
        Requested backend information based on return_type
    """
    if not return_type:
        return _AVAILABLE_BACKENDS
    
    if return_type == 'names':
        return tuple(_AVAILABLE_BACKENDS.keys())
    elif return_type == 'backends':
        return tuple(_AVAILABLE_BACKENDS.values())
    
    backend = _AVAILABLE_BACKENDS.get(return_type)
    if not backend:
        raise ValueError(f"Unknown backend: {return_type}")
    return backend


if __name__ == '__main__':
    import json
    from typing import Any

    def pretty_print(data: Union[Dict[str, Any], list, MappingProxyType]) -> None:
        """Print data in a formatted JSON structure."""
        if isinstance(data, MappingProxyType):
            data = dict(data)
        print(json.dumps(data, indent=4, default=str))

    # Test backend configurations
    print("Available backends:")
    pretty_print(get_available_backends())
    
    print("\nBackend names:")
    print(get_available_backends('names'))
    
    print("\nTesting specific backend:")
    try:
        openai_backend = get_available_backends('openai')
        print(f"OpenAI backend: {openai_backend}")
    except ValueError as e:
        print(f"Error: {e}")
