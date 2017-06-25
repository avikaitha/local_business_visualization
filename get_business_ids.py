from pymongo import MongoClient
import json
from bson import json_util

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'yelp_dataset'
COLLECTION_NAME = 'yelp_business'

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DB_NAME][COLLECTION_NAME]

fields = {'_id': False,'business_id': True}

query = {'city': 'Tempe'}
results = collection.find(query,projection=fields)
business_ids = []
f = open('business_ids.txt', 'w')
for result in results:
    try:
        business_ids += [result['business_id']]
        f.write(result['business_id']+"\n")
    except:
        pass

print len(business_ids)

connection.close()
f.close()
