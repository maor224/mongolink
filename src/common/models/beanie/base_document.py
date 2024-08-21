from beanie import Document
from typing import TypeVar, Generic
from src.common.models.base_model import AbstractModel

T = TypeVar("T", bound=AbstractModel)


class BaseDocument(Document, Generic[T]):
    class Settings:
        abstract = True
