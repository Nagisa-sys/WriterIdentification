import pymongo
from datetime import datetime


client = pymongo.MongoClient("mongodb+srv://flask_app:flask_app@aioperations.75psp.mongodb.net/flask_app?retryWrites=true&w=majority")
db = client.get_database('AIOperations')
operations_collection = pymongo.collection.Collection(db, 'Operations')

def to_date(date_string): 
	try:
		date_formated = datetime.strptime(date_string, "%Y-%m-%d").date()
		return datetime(date_formated.year, date_formated.month, date_formated.day)
		date_formated
	except ValueError:
		raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))
	
min_date = to_date("2020-09-01")
max_date = to_date("2020-09-04")

pipeline = [
    {"$match": { "date" :{ "$gte":min_date, "$lt":max_date} }},
    {"$group": {
		"_id": { "$dateToString": { "format": "%Y-%m-%d", "date": "$date" } }, 
		"totalSum": {"$sum": 1},
		"totalClaimed": {
			"$sum":{
				"$cond": ["$claimedFalse", 1, 0]
			}
		}
	}},
	{"$addFields": { "date": "$_id" }},
	{"$project": { "_id": 0 }}
]

result = list(operations_collection.aggregate(pipeline))
#result = list(operations_collection.find({}))

print(result)