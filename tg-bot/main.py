import logging
from aiogram import executor
from loader import dp
import handlers


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    executor.start_polling(dp)