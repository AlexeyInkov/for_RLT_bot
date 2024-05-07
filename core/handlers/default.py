from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hlink

router = Router()


@router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer("".join(("Hi ", hlink(message.from_user.full_name, message.from_user.url), "!")))
