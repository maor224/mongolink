from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import TypeVar, Generic
from src.common.models.beanie.base_document import BaseDocument
from src.common.collection_controller import GenericCollectionController
from src.common.mongo_connection import MongoDBConnection
from src.common.models.base_model import AbstractModel
from beanie import init_beanie

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = MongoDBConnection()
    await connection.initialize_client()  # Replace with your database name

    # Initialize Beanie with the database
    db = await connection.get_database("users")
    await init_beanie(db, document_models=[UserDocument])  # Assuming UserDocument is your Beanie model

    yield

    # Close the connection when the app shuts down
    await connection.client.close()

app = FastAPI(lifespan=lifespan)

# Type variables
M = TypeVar("M", bound=AbstractModel)
D = TypeVar("D", bound=BaseDocument[M])

# Global connection object
connection = None


# Define a User model and document
class User(AbstractModel):
    name: str
    email: str


class UserDocument(BaseDocument[User]):
    name: str
    email: str

    class Settings:
        collection = "users"


class GenericAPI(Generic[M, D]):
    def __init__(
        self, collection_controller: GenericCollectionController[M, D], db_name: str
    ):
        self.controller = collection_controller
        self.db_name = db_name
        self.create_routes("users")

    def create_routes(self, model_name: str):
        @app.post(f"/{model_name}/")
        async def create_document(model: User):
            try:
                return await self.controller.create(**model.model_dump())
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @app.get(f"/{model_name}/{{id}}")
        async def get_document(id: str):
            try:
                return await self.controller.get(id)
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

        @app.put(f"/{model_name}/{{id}}")
        async def update_document(id: str, model: User):
            try:
                return await self.controller.update(id, **model.dict())
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @app.delete(f"/{model_name}/{{id}}")
        async def delete_document(id: str):
            try:
                await self.controller.delete(id)
                return {"detail": "Document deleted"}
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))


# Initialize the controller with User as M
user_controller = GenericCollectionController[User, UserDocument](User, UserDocument)

# Create API instance with User as M and specify database name
db_name = "users"  # Replace with your actual database name
user_api = GenericAPI[User, UserDocument](user_controller, db_name)
