from pymongo import MongoClient

from config import client

client = MongoClient(client)
db = client["fam_data"]
collection = db['purchases']

def get_data(id, data): 
    doc = collection.find_one({"_id":id})
    if data == 'name':
        return doc['name']
    elif data == 'date':
        return doc['week']
    elif data == 'isactive':
        return doc['isactive']
    
def getAll() -> dict:
    posts = {}
    for post in collection.find({'isactive': True}):
        posts[post['_id']] = post['name']
    # {1: 'non', 2: 'pashtet'}
    return posts

def change_status(id): 
    status = get_data(id=id, data='isactive')
    if status:
        collection.update_one(collection.find_one({"_id": id}), {'$set': {'isactive': False}})
    else:
        collection.update_one(collection.find_one({"_id": id}), {'$set': {'isactive': True}})

def add_data(name, type='week'):
    new_doc = {
        '_id': collection.count_documents({})+1,
        'name': name,
        'type': type,
        "isactive": True
    }

    collection.insert_one(new_doc)
