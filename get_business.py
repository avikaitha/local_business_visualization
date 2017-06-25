from pymongo import MongoClient
import json
from bson import json_util
"""
{
    "_id" : ObjectId("58e440eab5cdde510902d99d"),
    "business_id" : "cE27W9VPgO88Qxe4ol6y_g",
    "full_address" : "1530 Hamilton Rd\nBethel Park, PA 15234",
    "hours" : {},
    "open" : false,
    "categories" : [
        "Active Life",
        "Mini Golf",
        "Golf"
    ],
    "city" : "Bethel Park",
    "review_count" : 5,
    "name" : "Cool Springs Golf Center",
    "neighborhoods" : [],
    "longitude" : -80.0146597,
    "state" : "PA",
    "stars" : 2.5,
    "latitude" : 40.3541155,
    "attributes" : {
        "Good for Kids" : true
    },
    "type" : "business"
}
"""
def get_businesses(state,category,collection):

    fields = {'_id': False,'name': True,'city':True,'stars':True,'review_count':True,'categories':True,'state': True}
    query = {'state': state,'categories':category}
    projects = collection.find(query,projection=fields)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    return json_projects
