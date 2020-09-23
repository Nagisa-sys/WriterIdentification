import numpy as np
from sklearn.cluster import MiniBatchKMeans

class Clusterer:

	@staticmethod
	def fit_ancient_data(path_centers):
		return np.load(path_centers)

	@staticmethod
	def fit_new_trainig(vectors, path_to_save=None, nb_clusters=300, max_no_improvement=1000, verbose=1, shuffle=True):
		if shuffle: np.random.shuffle(vectors)
		kmeans = MiniBatchKMeans(n_clusters = nb_clusters, verbose=verbose, max_no_improvement=max_no_improvement)
		kmeans.fit(vectors)

		if path_to_save is not None:
			np.save(path_to_save, kmeans.cluster_centers_)
		
		return kmeans

	@staticmethod
	def elbow_method_kmeans(vectors, max_no_improvement, test_values ,figsize=(15, 5), verbose=0):
		from matplotlib import pyplot as plt
        
		np.random.shuffle(vectors)
		distorsions = [Clusterer.fit_new_trainig(vectors, nb_clusters=k, max_no_improvement=max_no_improvement, verbose=verbose, shuffle=False).inertia_ for k in test_values]
		
		fig = plt.figure(figsize=figsize)
		plt.plot(test_values, distorsions, marker='o')
		plt.xticks(test_values)
		plt.xlabel('Number of clusters')
		plt.ylabel('Within-cluster sum of squares')
		plt.grid(True)
		plt.title('Elbow curve')