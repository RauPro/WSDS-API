import logging

from pymongo import MongoClient


class DatabaseService:
    """
    A singleton class for managing the connection to a MongoDB database.

    This class provides a centralized way to connect to a MongoDB database using the PyMongo library.
    It ensures that only one instance of the class is created and provides methods to access the
    database and its collections.

    Attributes:
        _instance (DatabaseService): The single instance of the DatabaseService class.
        client (MongoClient): The MongoDB client used for connecting to the database.
        db (Database): The reference to the connected database.

    Methods:
        __new__(cls): Creates and returns the single instance of the DatabaseService class.
        _initialize(cls): Initializes the MongoDB connection and sets the database reference.
        get_db(cls) -> Database: Returns the reference to the connected database.
        get_prompts_collection(cls) -> Collection: Returns the reference to the "prompts" collection.
        get_promptEntry_collection(cls) -> Collection: Returns the reference to the "promptsEntry" collection.
        get_news_collection(cls) -> Collection: Returns the reference to the "news" collection.
        get_sheets_collection(cls) -> Collection: Returns the reference to the "sheets" collection.
        get_global_collection(cls) -> Collection: Returns the reference to the "global" collection.

    Example:
        # Get the single instance of DatabaseService
        db_service = DatabaseService()

        # Access the database
        db = db_service.get_db()

        # Access a specific collection
        prompts_collection = db_service.get_prompts_collection()
    """
    _instance = None
    client = None  # MongoDB client
    db = None  # Database reference

    def __new__(cls):
        """
        Creates and returns the single instance of the DatabaseService class.

        If an instance already exists, it is returned. Otherwise, a new instance is created
        and the MongoDB connection is initialized.

        Returns:
            DatabaseService: The single instance of the DatabaseService class.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        """
        Initializes the MongoDB connection and sets the database reference.

        This method establishes a connection to the MongoDB server using the provided connection string
        and sets the database reference to the specified database name.

        Raises:
            Exception: If an error occurs while connecting to the MongoDB server.
        """
        try:
            logging.info("Initializing MongoDB connection...")
            cls.client = MongoClient(
                "mongodb+srv://RauPro:rGe6DOPAZwAswTsl@wsds.xelacfb.mongodb.net/?retryWrites=true&w=majority&appName=WSDS")
            cls.db = cls.client["wsds-database"]  # Setting the db to specific database name
            logging.info("MongoDB connected to wsds-database.")
        except Exception as e:
            logging.error("Failed to connect to MongoDB", exc_info=True)
            raise e

    @classmethod
    def get_db(cls):
        """
        Returns the reference to the connected database.

        Returns:
            Database: The reference to the connected database.

        Raises:
            Exception: If the database is not initialized.
        """
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db

    @classmethod
    def get_prompts_collection(cls):
        """
        Returns the reference to the "prompts" collection.

        Returns:
            Collection: The reference to the "prompts" collection.

        Raises:
            Exception: If the database is not initialized.
        """
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db["prompts"]

    @classmethod
    def get_prompt_entry_collection(cls):
        """
        Returns the reference to the "promptsEntry" collection.

        Returns:
            Collection: The reference to the "promptsEntry" collection.

        Raises:
            Exception: If the database is not initialized.
        """
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db["promptsEntry"]

    @classmethod
    def get_news_collection(cls):
        """
        Returns the reference to the "news" collection.

        Returns:
            Collection: The reference to the "news" collection.

        Raises:
            Exception: If the database is not initialized.
        """
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db["news"]

    @classmethod
    def get_sheets_collection(cls):
        """
        Returns the reference to the "sheets" collection.

        Returns:
            Collection: The reference to the "sheets" collection.

        Raises:
            Exception: If the database is not initialized.
        """
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db["sheets"]

    @classmethod
    def get_global_collection(cls):
        """
        Returns the reference to the "global" collection.

        Returns:
            Collection: The reference to the "global" collection.

        Raises:
            Exception: If the database is not initialized.
        """
        if cls.db is None:
            logging.error("Database not initialized.")
            raise Exception("Database is not initialized.")
        return cls.db["global"]
