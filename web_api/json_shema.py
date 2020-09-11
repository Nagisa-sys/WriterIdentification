import json
import jsonschema
from jsonschema import validate

operation_types = {"writer" : ["SDVP", "SEVP", "SDB"], "faceInPicture": ["face_recognition"], "faceInVideo":["face_recognition"]}

operationSchema = {
    "type": "object",
    "properties": {
        "operation_type": {
			"type": "string",
			"enum" : list(operation_types.keys())
		},
        "algo": {
			"type": "string",
			"enum" : sum(list(operation_types.values()),[])
		},
        "target": {"type": "string"},
		"references": {
			"type": "array",
			"minItems": 1,
			"items": [ {"url": { "type": "string"}}, {"label": { "type": "string"}}]
		}
    }
}

def validateJsonOperation(jsonData):
	try:
		validate(instance=jsonData, schema=operationSchema)
	except jsonschema.exceptions.ValidationError as err:
		return False
	if jsonData["algo"] not in operation_types[jsonData["operation_type"]]:
		return False
	return True
