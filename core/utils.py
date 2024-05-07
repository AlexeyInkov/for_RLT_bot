import calendar
import json
from datetime import datetime, timedelta
from json import JSONDecodeError

# INPUT_MONTH = '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-30T23:59:00", "group_type": "month"}'
# INPUT_DAY = '{"dt_from": "2022-10-01T00:00:00","dt_upto": "2022-10-02T23:59:00","group_type": "day"}'
# INPUT_HOUR = '{"dt_from": "2022-02-01T00:00:00","dt_upto": "2022-02-02T00:00:00","group_type": "hour"}'


def get_date_from_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


def get_str_from_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S")


async def check_input(input_str: str) -> tuple[bool, str] | tuple[bool, tuple]:
    try:
        input_dict = json.loads(input_str)
    except JSONDecodeError:
        return False, "Не преобразовать в словарь"
    try:
        if set(input_dict.keys()) != {"dt_from", "dt_upto", "group_type"}:
            raise KeyError
    except KeyError:
        return False, "Не правильные ключи словаря"
    try:
        check = (
            get_date_from_str(input_dict["dt_from"]),
            get_date_from_str(input_dict["dt_upto"]),
            input_dict["group_type"],
        )
        if check[0] > check[1]:
            raise ValueError
        if check[2] not in {"hour", "day", "month"}:
            raise ValueError
    except ValueError:
        return False, "Не правильные значения по ключам"
    else:
        return True, check


def get_labels(dt_from: datetime, dt_upto: datetime, group_type: str) -> list[str]:
    labels = []
    while dt_from <= dt_upto:
        labels.append(get_str_from_date(dt_from))
        if group_type == "hour":
            dt_from += timedelta(seconds=3600)
        elif group_type == "day":
            dt_from += timedelta(days=1)
        else:
            days_in_month = calendar.monthrange(dt_from.year, dt_from.month)[1]
            dt_from += timedelta(days=days_in_month)

    labels.append(get_str_from_date(dt_upto + timedelta(seconds=1)))
    return labels


def get_dataset(
    aggregate_collection, dt_from: datetime, labels: list[str]
) -> list[int]:
    answer_dict = dict()
    for item in aggregate_collection:
        answer_dict[get_str_from_date(dt_from + timedelta(seconds=item["_id"]))] = item[
            "total"
        ]
    return [answer_dict.get(key, 0) for key in labels[:-1]]
