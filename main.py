import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import BOT_TOKEN
from core.handlers.custom import router as custom_router
from core.handlers.default import router as default_router


async def main() -> None:
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(default_router, custom_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
