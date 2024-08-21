import threading

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from src.config.settings.connection import ConnectionSettings


class MongoDBConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MongoDBConnection, cls).__new__(
                    cls, *args, **kwargs
                )
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.settings = ConnectionSettings()
            self.client = None
            self.initialized = True

    async def initialize_client(self):
        if self.client is None:
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

    async def get_collection(
        self, database_name: str, collection_name: str
    ) -> AsyncIOMotorCollection:
        database = await self.get_database(database_name)
        return database[collection_name]
