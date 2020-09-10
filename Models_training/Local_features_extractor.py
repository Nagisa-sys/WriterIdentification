import numpy as np
import cv2

class Local_feature_exractor:

	def __init__(self, normalization, local_feature_extractor=cv2.xfeatures2d.SIFT_create()):
		self.local_feature_extractor = local_feature_extractor
		self.normalization = normalization

	def kps_descriptors(self, image):
		kps, descriptors = self.local_feature_extractor.detectAndCompute(image, None)
		kps_cleaned = list()
		descriptors_cleaned = list()

		for key_point, descriptor in zip(kps, descriptors):
			if self.filter(image, key_point):
				kps_cleaned.append(key_point)
				descriptors_cleaned.append(descriptor)

		descriptors_cleaned = self.normalization(descriptors_cleaned)

		return kps_cleaned, descriptors_cleaned

	def filter(self, image, key_point):
		y,x = int(key_point.pt[0]),int(key_point.pt[1])
		s = int(key_point.size/2)
		Sn = np.sum(image[y-s:y+s,x-s:x+s]==0)
		if (Sn >= (s-1)):	return True
		return False