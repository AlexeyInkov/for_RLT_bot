from datetime import datetime

from pymongo import MongoClient, collection

from core.config import HOST, PORT, DB_NAME, COLLECTION_NAME
from core.utils import get_date_from_str


def get_collection() -> collection:
    client = MongoClient(HOST, PORT)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


def get_aggregate_collection(
    my_collection: collection, dt_from: datetime, dt_upto: datetime, labels: list[str]
) -> collection:
    boundaries = [0]
    for index in range(1, len(labels)):
        delta = get_date_from_str(labels[index]) - dt_from
        boundaries.append(delta.total_seconds())

    pipeline = [
        {"$match": {"dt": {"$lte": dt_upto, "$gte": dt_from}}},
        {
            "$set": {
                "diff": {
                    "$dateDiff": {
                        "startDate": dt_from,
                        "endDate": "$dt",
                        "unit": "second",
                    }
                }
            }
        },
        {
            "$bucket": {
                "groupBy": "$diff",
                "boundaries": boundaries,
                "output": {"total": {"$sum": "$value"}},
            }
        },
    ]
    return my_collection.aggregate(pipeline)
