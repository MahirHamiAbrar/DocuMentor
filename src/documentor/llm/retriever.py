from loguru import logger
from .prompts import *
from .groq_model import GroqModel


class Retriever(GroqModel):
    def __init__(self) -> None:
        GroqModel.__init__(self)
