import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from datetime import datetime

class MongoDb_Operations_Storage:
	def __init__(self, connection_string):
		client = pymongo.MongoClient(conection_string)
		db = client.get_database('AIOperations')
		self.operations_collection = pymongo.collection.Collection(db, 'Operations')

	def save_operation(self, json_object):
		inserted_id = self.operations_collection.insert_one(json_object).inserted_id
		return inserted_id

	def get_operation_id(self, inserted_id):
		result = self.operations_collection.find_one({'_id': ObjectId(inserted_id), "deleated":False },{"_id" : 0, "deleated":0})
		if result :
			result['id'] = str(inserted_id)
			result['date'] = result["date"].strftime("%Y-%m-%d %H:%M:%S")
			result = dumps(result, json_options=RELAXED_JSON_OPTIONS)
		return result

	def delete_operation_id(self, id):
		result = self.operations_collection.update_one({"_id":ObjectId(id), "deleated":False}, {"$set":{"deleated":True}}) 
		if result.modified_count==1:
			return id
		return None

	def claim_false_operation_id(self, id, value):
		result = self.operations_collection.update_one({"_id":ObjectId(id), "deleated":False}, {"$set":{"claimedFalse":value}}) 
		if result.modified_count==1 or result.matched_count==1:
			return id
		return None


	def prepare_operation_data_json(self, operation_data, results):
		operation_data['deleated']=False
		operation_data['revised']=False
		operation_data['claimedFalse']=False
		operation_data['date']= datetime.now()
		operation_data['results']=results
		
		return operation_data

	def indicators(self, start_date, end_date):
		pipeline = [
			{"$match": { "date" :{ "$gte":start_date, "$lt":end_date} }},
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
		return list(self.operations_collection.aggregate(pipeline))


conection_string = ""
mongoDb_Operations_Storage = MongoDb_Operations_Storage(conection_string)