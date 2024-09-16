from pymongo import MongoClient
from pymongo.collection import Collection
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
schedule_collection = db.schedule

def init_db():
    # Create an index on 'title' and 'time' to ensure uniqueness if needed
    schedule_collection.create_index([('title', 1), ('time', 1)], unique=True)

def update_database(schedule):
    # Clear existing data
    schedule_collection.delete_many({})
    # Insert new data
    for anime in schedule:
        schedule_collection.insert_one({
            'title': anime['title'],
            'time': anime['time'],
            'released': False
        })

def check_for_releases(schedule):
    for anime in schedule:
        schedule_collection.update_one(
            {'title': anime['title'], 'time': anime['time']},
            {'$set': {'released': True}}
        )

def create_schedule_message():
    cursor = schedule_collection.find()
    message = ""
    for doc in cursor:
        status = "✅" if doc['released'] else "📅"
        message += f"{doc['title']} - {doc['time']} {status}\n"
    return message
