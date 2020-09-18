import os, cv2
import matplotlib.pyplot as plt
import numpy as np
import requests

class Image :

	def __init__(self, image_path, local_feature_extractor, global_feature_extractor=None, image_filter=None, url=False, verbose=False):
		self.name = os.path.splitext(os.path.basename(image_path))[0]
		self.path = image_path
		if url:
			self.image = self.read_image_gray(self.fetch_from_url(image_path))
		else:
			self.image = self.read_image_gray(cv2.imread(image_path))
		self.key_points, self.local_descriptors = local_feature_extractor.kps_descriptors(self.image)
		if image_filter is not None:
			image_filter(self.image)
		if global_feature_extractor is not None:
			self.set_global_descriptor(global_feature_extractor)
		if verbose : print("I have prepared an image !")

	def fetch_from_url(self, image_path):
		resp = requests.get(image_path, stream=True).raw
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		return image

	def set_global_descriptor(self, global_feature_extractor):
		self.global_descriptor = global_feature_extractor.global_feature_vector(self.local_descriptors)

	def has_global_descriptor(self):
		if not hasattr(self, 'global_descriptor'):
			return False
		return True

	def read_image_gray(self, image_path, margin=40):
		return cv2.cvtColor(image_path,cv2.COLOR_BGR2GRAY)[:,margin:-margin]

	def draw_image_key_points(self, figsize=(20,20)):
		drawing = cv2.drawKeypoints(self.image,self.key_points,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		plt.figure(figsize=figsize)
		plt.imshow(drawing)
		plt.title("keypoints")
		plt.show()

	def save_image_key_points(self, path="./result.png"):
		drawing = cv2.drawKeypoints(self.image,self.key_points,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(path, drawing)