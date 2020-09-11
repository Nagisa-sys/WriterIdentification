from flask import Flask, request, jsonify, Response, make_response
from services_AI import identification_operation
from services_history import getOperation, deleteOperation, claimFUpdateOperation, get_indicators
import argparse

parser = argparse.ArgumentParser(description='launch flask server')
parser.add_argument('--public', required=False, help='use pyngrok server', action='store_true')
args = parser.parse_args()

app = Flask(__name__)
#app.config["DEBUG"] = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/v0/operation', methods=['POST', 'GET', 'PUT', 'DELETE'])
def ai_operation():
	if request.method == 'POST': 
		return identification_operation(request.json)
	if request.method == 'GET':
		if 'id' in request.args:
			return getOperation(str(request.args['id']))
		else:
			return jsonify({"message":"No id provided"}), 400
	if request.method == 'DELETE':
		if 'id' in request.args:
			return deleteOperation(str(request.args['id']))
		else:
			return jsonify({"message":"No id provided"}), 400
	if request.method == 'PUT':
		id = request.args.get("id")
		if not id : return jsonify({"message":"No id provided"}), 400
		new_value = request.args.get("new_value")
		if not new_value : return jsonify({"message":"No new_value provided"}), 400
		if new_value not in ["false","true"] : return jsonify({"message":"new_value must either false or true"}), 400
		return claimFUpdateOperation(id, new_value)


@app.route('/api/v0/operations', methods=['GET'])
def indicators():
	if 'start' in request.args:
		try:
			return get_indicators(request.args)
		except ValueError as ex:
			return jsonify({'message': str(ex)}), 400 
	else:
		return jsonify({"message":"No start date provided"}), 400


if __name__ == '__main__':
	port = 8000
	if args.public:
		from pyngrok import ngrok
		url = ngrok.connect(port)
		print(' * Tunnel URL:', url)
	app.run(port=port)