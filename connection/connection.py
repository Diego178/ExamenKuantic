import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

uri = os.getenv('URI_DB')
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

db = client.movies_database
collection_movies = db.collection_movies
collection_users = db.collection_users


async def ping_server():
  try:
      await client.admin.command('ping')
      print("Connection successful to DataBase")
  except Exception as e:
      print("Error in the connection: " + str(e))





