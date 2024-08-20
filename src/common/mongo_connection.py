import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config.settings.connection import ConnectionSettings


class MongoDBConnection:
    def __init__(self):
        self.settings = ConnectionSettings()
        self.client = None

    async def initialize_client(self):
        connection_string = await self.get_connection_string()
        self.client = AsyncIOMotorClient(connection_string)

    async def get_connection_string(self) -> str:
        return f"mongodb+srv://{self.settings.username}:{self.settings.password}@{self.settings.host}"

    async def get_database(self, database_name: str) -> AsyncIOMotorDatabase:
        if not self.client:
            raise ValueError(
                "Client is not initialized. Call `initialize_client` first."
            )
        return self.client[database_name]

    async def create_collection(self, database_name: str, collection_name: str) -> None:
        database = await self.get_database(database_name)
        await database.create_collection(collection_name)
