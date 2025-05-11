from dotenv import load_dotenv
from typing import Any, List, Union, Literal, Optional

load_dotenv()   # load all environment variables

from openai import OpenAI
from openai.types import Model
from openai.types.chat.chat_completion import ChatCompletion

from documentor_ai.backends import (
    BackendInfo,
    get_available_backends,
)
from documentor_ai._types import Messages


class ChatModel:
    _model_name: str = None

    def __init__(
        self,
        backend: Literal['groq', 'openai', 'nvidia-nim']
    ) -> None:
        
        self._backend_info: BackendInfo = get_available_backends(backend)

        self._client: OpenAI = OpenAI(
            api_key=self._backend_info.api_key,
            base_url=self._backend_info.base_url
        )
    
    @property
    def model_name(self) -> str:
        return (
            self._model_name
            if self._model_name
            else self._backend_info.default_model_name
        )
    
    @model_name.setter
    def model_name(self, name: str) -> None:
        assert self.is_valid_model(name), 'Invalid Model!'
        self._model_name = name
    
    def get_model_list(
        self, 
        return_type: Optional[Literal['id', 'json']] = None
    ) -> Union[List[dict[str, Any]] | List[str] | List[Model]]:
        
        models = self._client.models.list().data
        
        if return_type == 'json':
            return [
                model.model_dump(mode='json')
                for model in models
            ]
        
        elif return_type == 'id':
            # The api always returns model list in an arbitary order.
            # So, id - sorting is required as these names might be 
            # used in such places where consistancy is necessary.
            return sorted([
                model.id
                for model in models
            ])
        
        return models
    
    def is_valid_model(self, model_name: str) -> bool:
        for model in self.get_model_list():
            if model_name == model.id:
                return True
        return False
    
    def generate_response(self,
        messages: Messages,
        stream: bool = False,
    ) -> str:
        response: ChatCompletion = self._client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            stream=stream
        )

        response_text: str = ""

        if stream:
            for chunk in response:
                chunk_text = chunk.choices[0].delta.content
                if chunk_text:
                    response_text += chunk_text
        else:
            response_text = response.choices[0].message.content
        
        return response_text


if __name__ == '__main__':
    from documentor_ai.messages import ChatMessages
    
    cm = ChatModel(backend='nvidia-nim')
    # print(cm.get_model_list('json'))

    cms = ChatMessages()
    cms.add_user_message('What do you mean by Paraphrasing?')

    print(cm.generate_response(messages=cms.messages()))
