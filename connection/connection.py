import asyncio
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

async def ping_server():
  uri = os.getenv('URI_DB')
  client = AsyncIOMotorClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
  try:
      await client.admin.command('ping')
      print("Connection successful to DataBase")
  except Exception as e:
      print("Error in the connection: " + str(e))

asyncio.run(ping_server())