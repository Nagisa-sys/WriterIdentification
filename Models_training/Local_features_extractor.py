import numpy as np
import cv2

class Local_feature_extractor:

	def __init__(self, algorithm, norm=lambda x:x):
		self.algorithm = algorithm
		self.norm = norm

	def kps_descriptors(self, image):
		kps, descriptors = self.algorithm.detectAndCompute(image, None)
		kps_cleaned = list()
		descriptors_cleaned = list()

		binary_image = self.binarize_image(image)

		for key_point, descriptor in zip(kps, descriptors):
			if self.filter(binary_image, key_point):
				kps_cleaned.append(key_point)
				descriptors_cleaned.append(descriptor)

		descriptors_cleaned = self.norm(descriptors_cleaned)

		return kps_cleaned, descriptors_cleaned

	def binarize_image(self, image):
		blur = cv2.GaussianBlur(image,(5,5),0)
		_, binary_image = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		return binary_image

	def kps(self, image):
		kps = self.algorithm.detect(image, None)
		kps_cleaned = list()
		binary_image = self.binarize_image(image)
		for key_point in kps:
			if self.filter(binary_image, key_point):
				kps_cleaned.append(key_point)
		return kps_cleaned

	def filter(self, binary_image, key_point):
		y,x = int(key_point.pt[0]),int(key_point.pt[1])
		if binary_image[x,y]==0: return True
		return False