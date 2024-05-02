from services.db_service import DatabaseService

class NewsService:
    @staticmethod
    def save_news(news_data):
        news_collection = DatabaseService.get_db()['news']

        insert_result = news_collection.insert_one(news_data)
        return insert_result.inserted_id