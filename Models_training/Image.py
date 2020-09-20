import os, cv2
import matplotlib.pyplot as plt
import numpy as np

class Image :
	def __init__(self, image, local_feature_extractor, image_name="", global_feature_extractor=None, image_filter=None, verbose=False):
		self.name = image_name
		self.image = image
		self.key_points, self.local_descriptors = local_feature_extractor.kps_descriptors(self.image)
		if image_filter is not None:
			image_filter(self.image)
		if global_feature_extractor is not None:
			self.set_global_descriptor(global_feature_extractor)
		if verbose : print("I have prepared an image !")

	def set_global_descriptor(self, global_feature_extractor):
		self.global_descriptor = global_feature_extractor.global_feature_vector(self.local_descriptors)

	def has_global_descriptor(self):
		if not hasattr(self, 'global_descriptor'):
			return False
		return True

	def draw_image_key_points(self, figsize=(20,20)):
		drawing = cv2.drawKeypoints(self.image,self.key_points,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		plt.figure(figsize=figsize)
		plt.imshow(drawing)
		plt.title("keypoints")
		plt.show()

	def save_image_key_points(self, path="./result.png"):
		drawing = cv2.drawKeypoints(self.image,self.key_points,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(path, drawing)