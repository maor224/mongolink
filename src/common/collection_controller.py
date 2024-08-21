from typing import Type, TypeVar, Generic
from datetime import datetime, timezone
from src.common.models.base_model import AbstractModel
from src.common.models.beanie.base_document import BaseDocument

M = TypeVar("M", bound=AbstractModel)
D = TypeVar("D", bound=BaseDocument[M])


class GenericCollectionController(Generic[M, D]):
    model_class: Type[M]
    document_class: Type[D]

    def __init__(self, model_class: Type[M], document_class: Type[D]):
        self.model_class = model_class
        self.document_class = document_class

    async def create(self, **kwargs) -> D:
        model_instance = self.model_class(**kwargs)
        document_instance = self.document_class(**model_instance.dict())
        await document_instance.insert()
        return document_instance

    async def get(self, id: str) -> D:
        return await self.document_class.get(id)

    async def update(self, id: str, **kwargs) -> D:
        document_instance = await self.document_class.get(id)
        for key, value in kwargs.items():
            if key == "_id":
                continue
            if hasattr(document_instance, key):
                setattr(document_instance, key, value)
        document_instance.updated_at = datetime.now(timezone.utc)
        await document_instance.save()
        return document_instance

    async def delete(self, id: str) -> None:
        document_instance = await self.document_class.get(id)
        await document_instance.delete()
