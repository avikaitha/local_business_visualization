# coding=utf-8
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features
from pymongo import MongoClient
from bson import json_util
import traceback
from watson_developer_cloud import WatsonException

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'yelp_dataset'
COLLECTION_NAME = 'yelp_reviews'

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DB_NAME][COLLECTION_NAME]

"""
{
  "url": "https://gateway-a.watsonplatform.net/calls",
  "note": "It may take up to 5 minutes for this key to become active",
  "apikey": "3b0f6eb85a00b2dec415a36feb25217b25f12e54"
}

{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "5e531399-68de-43bd-b092-ab368848134a",
  "password": "xVRLtpXTnRPO"

  "_id" : ObjectId("58e440eab5cdde5109031945"),
    "business_id" : "JokKtdXU7zXHcr20Lrk29A",
    "full_address" : "1340 E 8th St\nSte 104\nTempe, AZ 85281"
}


{
    "_id" : ObjectId("58e44157b5cdde51090b1ff2"),
    "votes" : {
        "funny" : 0,
        "useful" : 0,
        "cool" : 1
    },
    "user_id" : "FLdun6KWwAh-gC8VHVZGCw",
    "review_id" : "z9jpSh81Xpxe9cEMx0sTQw",
    "stars" : 5,
    "date" : "2006-09-02",
    "text" : "A happening and exciting restaurant / bar.  The chicken wings appetizer with the oatmeal stout infused barbeque sauce is scrumptious.",
    "type" : "review",
    "business_id" : "JokKtdXU7zXHcr20Lrk29A"
}

find({"city": "Tempe","name": {$regex : ".*Buffalo.*"}})
"""

watson_creds = [{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "826811ba-d2ea-4cdf-b19e-177aef5ef225",
  "password": "aj1BLsgmLqTe"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "adf990e2-57a7-46e4-b4ba-8975cfc821d4",
  "password": "lot6GKGyeJax"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "34265ada-81d8-43be-a8d5-f34616139faf",
  "password": "MHJbQb7n7bfp"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "f984833f-f5ec-474e-9f04-7918c0d4eb03",
  "password": "EeC7oqEOzTyq"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "662cd217-1435-4171-8adf-837038f1688b",
  "password": "iocvi5WUJa1C"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "50c8e7ab-4121-40c6-ad0b-3da6fda97bb1",
  "password": "dxrJIEEXRjq2"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "85bfb796-0548-40fe-be3b-ef7bf003d9cc",
  "password": "gIulrU8NbYhb"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "2e4b5b0d-4bea-420f-acb5-3d4054076c5b",
  "password": "NpUMQyRtPXGV"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "44ef6c6a-59db-455a-a6b0-9c00ff4a0cec",
  "password": "2dfM2IwodoXx"
},
{
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": "593e9017-a538-4819-bb5d-aa80e1878ee3",
  "password": "7q0qTyBmfXH3"
}
                ]

cred_count = 0
with open('business_ids.txt','r') as f:
    business_ids = f.readlines()

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username=watson_creds[cred_count]["username"],
    password=watson_creds[cred_count]["password"])

for business_id in business_ids:
    business_id = business_id.split(',')
    business_id = business_id[0].strip('"')
    print business_id
    # business_id = "Rr233WRnykn1j-qU9KOzCg"
    fields = {'_id': False,'review_id': True,'text':True,'date':True,'stars': True}
    # query = {'business_id': business_id,"date": {"$gte": '2016-03',"$lt": '2016-04'}}
    query = {'business_id': business_id,"pos_keywords": {"$exists": False}}
    # print query
    db_results = collection.find(query, projection=fields)
    json_projects = []

    count = 0


    # print db_results
    for db_result in db_results:
        # print db_result
        review = db_result["text"]
        pos_keywords = []
        neg_keywords = []
        try:
            response = natural_language_understanding.analyze(
                text=review,
                features=[features.Keywords()])

            temp_keywords = []

            for word in response["keywords"]:
                if word['relevance'] > 0.5:
                    temp_keywords += [word['text']]
                    # if word['text'] not in keywords:
                    #     keywords[word['text']] = 1
                    # else:
                    #     keywords[word['text']] += 1

            # print temp_keywords

            response2 = natural_language_understanding.analyze(
                text=review,
                features=[features.Sentiment(targets=temp_keywords)])
            # print(json.dumps(response2, indent=2))
            for target in response2["sentiment"]["targets"]:
                if target["label"] == u'negative':
                    keywords = neg_keywords
                else:
                    keywords = pos_keywords
                keywords += [target["text"]]
                # if target["text"] not in keywords:
                #     keywords[target["text"]] = 1
                #     # print keywords
                # else:
                #     # print keywords[target["text"]]
                #     keywords[target["text"]] += 1

            collection.update({'review_id': db_result['review_id']}, {"$set": {"pos_keywords":pos_keywords,"neg_keywords":neg_keywords}}, upsert=False)
            count += 1
            if count % 100 == 0:
                print count,len(pos_keywords),len(neg_keywords)
        except WatsonException as err:
            traceback.print_exc()
            print str(err).split(',')[1].strip()
            if str(err).split(',')[1].strip() == "Code: 403":
                if cred_count == len(watson_creds):
                    exit()
                else:
                    cred_count += 1
                    natural_language_understanding = NaturalLanguageUnderstandingV1(
                        version='2017-02-27',
                        username=watson_creds[cred_count]["username"],
                        password=watson_creds[cred_count]["password"])



