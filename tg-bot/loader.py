import pymongo as pymongo
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, MONGO_HOST, DB_NAME
from motor import motor_asyncio

# Prepare bot
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# Prepare db
db_client: motor_asyncio.AsyncIOMotorClient = motor_asyncio.AsyncIOMotorClient(MONGO_HOST)
db = db_client[DB_NAME]
users = db["users"]
basket = db["basket"]
basket_supplier = db["basket_supplier"]
