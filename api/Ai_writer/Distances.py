from scipy import spatial
import numpy as np

class Distance:

	@staticmethod
	def cosine_distance(vector_A, vector_B):
		return spatial.distance.cosine(vector_A.flatten(), vector_B.flatten())

	@staticmethod
	def chi2_distance(A, B):
		chi = 0.5 * np.sum([((a - b) ** 2) / max(a + b, +1e-9) for (a, b) in zip(A, B)]) 
		return chi