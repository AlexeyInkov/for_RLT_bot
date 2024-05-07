import json

from aiogram import Router, F
from aiogram.types import Message

from core.db import get_collection, get_aggregate_collection
from core.utils import check_input, get_labels, get_dataset

router = Router()


async def get_answer(check_tuple: tuple) -> str:
    dt_from, dt_upto, group_type = check_tuple
    labels = get_labels(dt_from, dt_upto, group_type)
    collection = get_collection()
    aggregate_collection = get_aggregate_collection(
        collection, dt_from, dt_upto, labels
    )
    dataset = get_dataset(aggregate_collection, dt_from, labels)

    return json.dumps({"dataset": dataset, "labels": labels[:-1]})


@router.message(F.text)
async def aggregate_handler(message: Message) -> None:
    check = await check_input(message.text)
    if check[0]:
        answer = await get_answer(check[1])
    else:
        answer = (
            check[1]
            + """
\nДопустимо отправлять только следующие запросы:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}
{"dt_from": "2022-10-01T00:00:00","dt_upto": "2022-11-30T23:59:00","group_type": "day"}
{"dt_from": "2022-02-01T00:00:00","dt_upto": "2022-02-02T00:00:00","group_type": "hour"}
"""
        )
    await message.answer(answer)
