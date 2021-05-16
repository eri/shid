import pymongo

import extensions.config as config

mongo = pymongo.MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=100)

def find(db, collection, query):
    query = mongo[db][collection].find(query)
    if query and query.count() > 0:
        return query
    return None

def search_by_value(db, collection, filters):
    search = mongo.find(db, collection,
        {
            "$or": [{
                k: {"$regex": str(v), "$options": "i"}
            } for k, v in filters.items()
                # {"nom": {"$regex": query, "$options": "i"}},
                # {"prenom": {"$regex": query, "$options": "i"}},
            ]
        },
    )

def find_sorted(db, collection, query, sorter):
    query = mongo[db][collection].find(query).sort(sorter['k'], sorter['o'])
    return query

def insert_one(db, collection, data):
    query = mongo[db][collection].insert_one(data)
    if query:
        return query
    return None
