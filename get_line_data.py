import json


"""
{
    "field": "date",
    "value": "2012-12-28T00:00:00Z",
    "count": 15,
    "pivot": [{
        "field": "stars",
        "value": 3.0,
        "count": 5},
        {
            "field": "stars",
            "value": 4.0,
            "count": 4},
        {
            "field": "stars",
            "value": 1.0,
            "count": 3},
        {
            "field": "stars",
            "value": 2.0,
            "count": 2},
        {
            "field": "stars",
            "value": 5.0,
            "count": 1}]}
"""
with open("spiral_data.json",'r') as f:
    content = json.load(f)

print content


#
# averages = {}
#
#
# for result in content:
#     date = result["value"].split('T')[0]
#     review_count = result["count"]
#
#     pivot = result["pivot"]
#
#     sum = 0
#
#     for facet in pivot:
#         value = facet["value"]
#         count = facet["count"]
#
#         sum += value*count
#
#     avg = sum/review_count
#
#     averages[date] = avg
#
#
# import operator
#
# sorted_dates = sorted(averages.items(), key=operator.itemgetter(0))
# print sorted_dates
# print "date,close"
# for date,aver in sorted_dates:
#     print date+","+str(aver)