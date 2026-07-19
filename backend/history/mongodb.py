import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoDB:

    def __init__(self):

        uri = os.getenv("MONGODB_URI")
        database_name = os.getenv("DATABASE_NAME")

        self.client = MongoClient(uri)

        self.db = self.client[database_name]

        self.conversations = self.db["conversations"]
        self.complaints = self.db["complaints"]

mongodb = MongoDB()