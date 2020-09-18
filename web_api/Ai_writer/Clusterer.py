import numpy as np

class clusterer:

	@staticmethod
	def fit_ancient_data(path_centers):
		return np.load(path_centers)