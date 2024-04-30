import logging
from pymongo import MongoClient

class DatabaseService:
    _instance = None
    client = None  # MongoDB client
    db = None      # Database reference

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        try:
            logging.info("Initializing MongoDB connection...")
            cls.client = MongoClient("mongodb+srv://RauPro:rGe6DOPAZwAswTsl@wsds.xelacfb.mongodb.net/?retryWrites=true&w=majority&appName=WSDS")
            cls.db = cls.client["wsds-database"]  # Setting the db to specific database name
            logging.info("MongoDB connected to wsds-database.")
        except Exception as e:
            logging.error("Failed to connect to MongoDB", exc_info=True)
            raise e

    @classmethod
    def get_db(cls):
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db

    @classmethod
    def get_prompts_collection(cls):
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db["prompts"]
