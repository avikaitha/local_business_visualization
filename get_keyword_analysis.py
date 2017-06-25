from pymongo import MongoClient
import json
from bson import json_util

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'yelp_dataset'
COLLECTION_NAME = 'yelp_reviews'

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DB_NAME][COLLECTION_NAME]

fields = {'_id': False,'pos_keywords': True,'neg_keywords':True}

query = {'business_id': 'JokKtdXU7zXHcr20Lrk29A',"date": {"$gte": '2016-04',"$lt": '2016-05'}}
results = collection.find(query,projection=fields)
pos_keywords = {}
neg_keywords = {}
count = 0
for result in results:
    try:
        for keyword in result['neg_keywords']:
            if keyword not in neg_keywords:
                neg_keywords[keyword] = 1
            else:
                neg_keywords[keyword] += 1

        for keyword in result['pos_keywords']:
            if keyword not in pos_keywords:
                pos_keywords[keyword] = 1
            else:
                pos_keywords[keyword] += 1
    except:
        pass

print len(neg_keywords),len(pos_keywords)

import operator
pos_keywords = sorted(pos_keywords.items(), key=operator.itemgetter(1))

neg_keywords = sorted(neg_keywords.items(), key=operator.itemgetter(1))

count = 0

for tuple in reversed(pos_keywords):
    print '{ "name":"'+tuple[0]+'", years:'+str(tuple[1])+', "relevancy": 1 },'
    count += 1
    if count == 100:
        break
print "---------------------------------------"
"""
{ "name": "Java", years: 11, "relevancy": 1.3 }
"""
count = 0
for tuple in reversed(neg_keywords):
    print '{ "name":"' + tuple[0] + '", years:' + str(tuple[1]) + ', "relevancy": 1 },'
    count += 1
    if count == 100:
        break

connection.close()
