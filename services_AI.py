from Ai_writer.writer_Identifier import Writer_identification
from Ai_face.face_recogniser import *
from db import mongoDb_Operations_Storage
from json_shema import validateJsonOperation
from flask import jsonify, Response, make_response

writer_identifiere = Writer_identification()

def identification_operation(content):
	if not validateJsonOperation(content):
		return "Non conform json file", 400

	options = {
		"writer": identify_writer_operation,
		"faceInPicture": identify_face_image_operation,
		"faceInVideo": identify_face_video_operation
	}
	
	id, results = options[content["operation_type"]](content)
	response = {"id":id, "results":results}
	return make_response(jsonify(response), 200)


def extract_urls_labels(ref):
	images_ref, writers = [], []
	for element in ref:
		images_ref.append(element['url'])
		writers.append(element['label'])
	return images_ref, writers


def identify_writer_operation(operation):
	images_ref, writers = extract_urls_labels(operation["references"])
	mysterious_writer = writer_identifiere.predict(operation["algo"], images_ref, writers, operation["target"])
	operation_to_store = mongoDb_Operations_Storage.prepare_operation_data_json(operation, [mysterious_writer])
	return str(mongoDb_Operations_Storage.save_operation(operation_to_store)), mysterious_writer


def identify_face_image_operation(operation):
	images_ref, names = images_ref, writers = extract_urls_labels(operation["references"])
	mysterious_faces = face_recogniser.predict_image(images_ref, names, operation["target"])
	operation_to_store = mongoDb_Operations_Storage.prepare_operation_data_json(operation, mysterious_faces)
	return str(mongoDb_Operations_Storage.save_operation(operation_to_store)), mysterious_faces


def identify_face_video_operation(operation):
	images_ref, names = images_ref, writers = extract_urls_labels(operation["references"])
	mysterious_faces = face_recogniser.predict_video(images_ref, names, operation["target"])
	operation_to_store = mongoDb_Operations_Storage.prepare_operation_data_json(operation, mysterious_faces)
	return str(mongoDb_Operations_Storage.save_operation(operation_to_store)), mysterious_faces