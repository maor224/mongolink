from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from src.config.settings.connection import ConnectionSettings


class MongoDBConnection:

    def __init__(self):
        self.settings = ConnectionSettings()
        self.client = AsyncIOMotorClient(self.get_connection_string())

    def get_connection_string(self) -> str:
        return f"mongodb://{self.settings.username}:{self.settings.password}@{self.settings.mongodb_host}:{self.settings.port}"

    def get_database(self, database_name: str) -> AsyncIOMotorDatabase:
        return self.client[database_name]

    def get_collection(
        self, database_name: str, collection_name: str
    ) -> AsyncIOMotorCollection:
        database = self.get_database(database_name)
        return database[collection_name]
