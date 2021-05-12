import pymongo

mongo = pymongo.MongoClient("mongodb://mongodb:27017", serverSelectionTimeoutMS=100)

def find(db, collection, query):
    query = mongo[db][collection].find(query)
    if query and query.count() > 0:
        return query
    return None

def find_sorted(db, collection, query, sorter):
    query = mongo[db][collection].find(query).sort(sorter['k'], sorter['o'])
    return query

def insert_one(db, collection, data):
    query = mongo[db][collection].insert_one(data)
    if query:
        return query
    return None
