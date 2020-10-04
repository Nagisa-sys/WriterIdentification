from scipy import spatial
import numpy as np
import math

class Distance:

	@staticmethod
	def cosine_distance(A, B):
		return spatial.distance.cosine(A.flatten(), B.flatten())

	@staticmethod
	def chi2_distance(A, B):
		chi = 0.5 * np.sum([((a - b) ** 2) / max(a + b, +1e-9) for (a, b) in zip(A, B)]) 
		return chi

	@staticmethod
	def angular_distance(A, B):
		return math.acos(1-Distance.cosine_distance(A, B))/math.pi