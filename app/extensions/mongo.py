import pymongo

mongo = pymongo.MongoClient("localhost", 27017, serverSelectionTimeoutMS=100)

def find(db, collection, query):
    query = mongo[db][collection].find(query)
    if query and query.count() > 0:
        return query[0]
    return None

def insert_one(db, collection, data):
    query = mongo[db][collection].insert_one(data)
    if query and query.count() > 0:
        return query
    return None
