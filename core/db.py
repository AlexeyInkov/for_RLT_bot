from pymongo import MongoClient

from core.utils import get_date_from_str


def get_collection():
    client = MongoClient("localhost", 27017)
    db = client.sampleDB
    return db.sample_collection


def get_aggregate_collection(collection, dt_from, dt_upto, labels):
    boundaries = [0]
    for index in range(1, len(labels)):
        delta = get_date_from_str(labels[index]) - dt_from
        boundaries.append(delta.total_seconds())
    print(boundaries)  # TODO Убрать

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
    return collection.aggregate(pipeline)
