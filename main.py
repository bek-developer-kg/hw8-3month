import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    print("Бот запущен!")
    register_handlers(dp) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
