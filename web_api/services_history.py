from flask import jsonify, Response, make_response
from db import mongoDb_Operations_Storage
import datetime


def getOperation(id):
	response = mongoDb_Operations_Storage.get_operation_id(id)
	if response:
		return Response(response, mimetype="application/json", status=200)
	return prepare_result_message(id=id, successOp=False, key="message", value="can't find this operation")

def deleteOperation(id):
	id_deleted = mongoDb_Operations_Storage.delete_operation_id(id)
	if id_deleted:
		return prepare_result_message(id=id, successOp=True)
	return prepare_result_message(id=id, successOp=False, key="message", value="can't find this operation")

def claimFUpdateOperation(id, new_value):
	id_updated = mongoDb_Operations_Storage.claim_false_operation_id(id, new_value)
	if id_updated:
		return prepare_result_message(id, successOp=True, key="claimedFalse", value=new_value)
	return prepare_result_message(id=id, successOp=False, key="message", value="can't find this operation")

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


def prepare_result_message(id, successOp, key, value):
	if key : responseDict = { "id" : id, key : value }
	else : responseDict = None
	if successOp : 
		return make_response(jsonify(responseDict), 200)
	return make_response(jsonify(responseDict), 400)

