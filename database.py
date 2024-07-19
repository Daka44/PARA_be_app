from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")


def get_db() -> Database:
    """MongoDB 데이터베이스 연결 객체를 반환하는 함수"""
    client = MongoClient(MONGODB_URI)
    db = client["para7"]
    return db

