from json_shema import validateJsonClaimOperation
from flask import jsonify, Response, make_response
from db import mongoDb_Operations_Storage
import datetime


def getOperation(id):
	return Response(mongoDb_Operations_Storage.get_operation_id(id), mimetype="application/json", status=200)

def deleteOperation(id):
	successOp = mongoDb_Operations_Storage.delete_operation_id(id)==1
	return prepare_result_update(id, successOp, "deleted", True)

def claimFUpdateOperation(content):
	if not validateJsonClaimOperation(content):
		return "Non conform json file", 400
	successOp = mongoDb_Operations_Storage.claim_false_operation_id(content["id"], content["newValue"])==1
	
	return prepare_result_update(content["id"], successOp, "claimedFalse", content["newValue"])

def get_indicators(request_args):
	def to_date(date_string): 
		try:
			date_formated = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
			return datetime.datetime(date_formated.year, date_formated.month, date_formated.day)
			date_formated
		except ValueError:
			raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))

	start_date = to_date(request_args.get('start'))		
	end_date = to_date(request_args.get('end', default = datetime.date.today().isoformat()))
	response = mongoDb_Operations_Storage.indicators(start_date, end_date)
	return make_response(jsonify(response), 200)


def prepare_result_update(id, successOp, key, value):
	if successOp : 
		responseDict = { "id" : id, key : value }
		return make_response(jsonify(responseDict), 200)
	responseDict = { "error" : "operation not found" }
	return make_response(jsonify(responseDict), 400)

