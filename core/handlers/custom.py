from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text)
async def aggregate_handler(message: Message) -> None:
    answer = await get_answer()
    await message.answer(answer)
