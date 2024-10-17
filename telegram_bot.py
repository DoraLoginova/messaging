from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token='your-bot-token')
dp = Dispatcher(bot)

@dp.message_handler()
async def send_notification(message: str):
    # логика для обработки уведомлений
    pass

if __name__ == '__main__':
    executor.start_polling(dp)
