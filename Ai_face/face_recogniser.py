import face_recognition
import urllib, math, cv2

def produce_encoding_url(image_url):
	response = urllib.request.urlopen(image_url)
	image = face_recognition.load_image_file(response)

	return produce_encoding(image)

def produce_encoding(image):
	return face_recognition.face_encodings(image)


def predict_image(images_ref, names, image_target):
	detected_faces = []
	known_faces_encodings = []
	for image_url in images_ref:
		known_faces_encodings.append(produce_encoding_url(image_url)[0])
	
	target_face_encodings = produce_encoding_url(image_target)
	if len(target_face_encodings) == 0 :
		return detected_faces

	for face in target_face_encodings:
		matches = face_recognition.compare_faces(known_faces_encodings, face)
		if True in matches:
			first_match_index = matches.index(True)
			detected_faces.append(names[first_match_index])

	return detected_faces

def predict_video(images_ref, names, video_target):
	detected_faces = []
	known_faces_encodings = []
	target_face_encodings = []
	target_frames = get_video_frames(video_target)

	for image_url in images_ref:
		known_faces_encodings.append(produce_encoding_url(image_url)[0])
	for frame in target_frames:
		target_face_encodings.extend(produce_encoding(frame))

	for face in target_face_encodings:
		matches = face_recognition.compare_faces(known_faces_encodings, face)
		if True in matches:
			first_match_index = matches.index(True)
			if names[first_match_index] not in detected_faces:
				detected_faces.append(names[first_match_index])

	return detected_faces


def get_video_frames(video_url, seconds=5):
	frames = []
	vidcap = cv2.VideoCapture(video_url)
	success,image = vidcap.read()

	fps = vidcap.get(cv2.CAP_PROP_FPS)
	multiplier = int(fps * seconds)

	while success:
		frameId = int(round(vidcap.get(1)))
		success, image = vidcap.read()

		if frameId % multiplier == 0:
			frames.append(image)

	vidcap.release()
	return frames