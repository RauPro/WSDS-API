from pymongo import MongoClient

class DatabaseService:
    client = None
    db = None

    @staticmethod
    def initialize():
        DatabaseService.client = MongoClient("mongodb://localhost:27017/")
        DatabaseService.db = DatabaseService.client['wsds-database']
    
    @staticmethod
    def get_db():
        return DatabaseService.db
