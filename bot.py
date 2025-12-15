from aiogram import Bot, Dispatcher
from logging import basicConfig, INFO
from config import API_TOKEN    
from database import conn  
from asyncio import run 
from message import router as message_router    

basicConfig(level=INFO)

dp = Dispatcher()
dp.include_router(message_router)

async def main():
    bot = Bot(token=API_TOKEN)  
    await conn.init()
    try:
        await dp.start_polling(bot)    
    finally:
        await conn.close()    

if __name__ == '__main__':
    run(main()) 