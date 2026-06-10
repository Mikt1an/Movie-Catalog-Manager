import os
from datetime import datetime
from urllib.parse import quote_plus

import dotenv
from pymongo import MongoClient

dotenv.load_dotenv()


class LogWriter:
    """
    MongoDB context manager for storing and retrieving
    search history for Sakila Movie Explorer.

    Environment variables:
       DB_HOST_MONGO: Database host.
       DB_USER_MONGO: Database username.
       DB_PASSWORD_MONGO: Database password.
       DB_NAME_MONGO: Database name.

   Handles:
        - database connection
        - query execution
        - transaction commits
    """

    COLLECTION_NAME = "final_project_121225_anton_samoilenko"

    def __init__(self):
        user = quote_plus(os.getenv("DB_USER_MONGO"))
        password = quote_plus(os.getenv("DB_PASSWORD_MONGO"))
        host = os.getenv("DB_HOST_MONGO")
        db_name = os.getenv("DB_NAME_MONGO")

        mongo_uri = (
            f"mongodb://{user}:{password}@{host}/"
            f"?readPreference=primary"
            f"&ssl=false"
            f"&authMechanism=DEFAULT"
            f"&authSource={db_name}"
        )

        self.__client = MongoClient(mongo_uri)
        self.__db = self.__client[db_name]
        self._collection = self.__db[LogWriter.COLLECTION_NAME]

    def __enter__(self):
        self.__client.admin.command("ping")
        print("Connection MongoDB successful!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()
        return False

    def save_search_query(self, search_type, query_data, total_results):
        document = {
            "search_type": search_type,
            "query_data": query_data,
            "total_results": total_results,
            "created_at": datetime.now()
        }

        self._collection.insert_one(document)

    def get_popular_queries(self, limit=5):
        pipeline = [
            # Group identical queries and count occurrences
            {
                "$group": {
                    "_id": "$query_data",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        return list(self._collection.aggregate(pipeline))

    def get_last_queries(self, limit=5):
        return list(
            self._collection.find()
            .sort("created_at", -1)
            .limit(limit)
        )