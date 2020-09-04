from flask import Flask, request, jsonify, Response, make_response
from services_AI import identification_operation
from services_history import getOperation, deleteOperation, claimFUpdateOperation, get_indicators

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v0/operation', methods=['POST', 'GET', 'PUT', 'DELETE'])
def identify_writer_face():
	if request.method == 'POST':
		return identification_operation(request.json)
	if request.method == 'GET':
		if 'id' in request.args:
			return getOperation(str(request.args['id']))
		else:
			return Response({"error":"No id provided"}, mimetype="application/json", status=400)
	if request.method == 'DELETE':
		if 'id' in request.args:
			return deleteOperation(str(request.args['id']))
		else:
			return Response({"error":"No id provided"}, mimetype="application/json", status=400)
	if request.method == 'PUT':
		return claimFUpdateOperation(request.json)


@app.route('/api/v0/operations', methods=['GET'])
def indicators():
	if 'start' in request.args:
		try:
			return get_indicators(request.args)
		except ValueError as ex:
			return make_response(jsonify({'error': str(ex)}), 400 )
	else:
		return Response({"error":"No start date provided"}, mimetype="application/json", status=400)


if __name__ == '__main__':
    app.run(port=8000)