import numpy as np
from sklearn.cluster import MiniBatchKMeans

class Clusterer:

	@staticmethod
	def fit_ancient_data(path_centers):
		return np.load(path_centers)

	@staticmethod
	def fit_new_trainig(images, path_to_save=None, nb_clusters=300, max_no_improvement=1000, verbose=1):
		descriptor_list = []
		[descriptor_list.extend(image.local_descriptors) for image in images]
		np.random.shuffle(descriptor_list)
		
		kmeans = MiniBatchKMeans(n_clusters = nb_clusters, verbose=verbose, max_no_improvement=max_no_improvement)
		kmeans.fit(descriptor_list)

		if path_to_save is not None:
			np.save(path_to_save, kmeans.cluster_centers_)
		
		return kmeans.cluster_centers_