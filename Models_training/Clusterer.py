import numpy as np
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn_extra.cluster import KMedoids
from sklearn import metrics
from matplotlib import pyplot as plt

class Clusterer:

	@staticmethod
	def fit_new_trainig(vectors, algo, metric, path_to_save=None, nb_clusters=300, max_no_improvement=1000, verbose=1, shuffle=True):
		assert algo in ['MiniBatchKMeans', 'KMedoids']
		if shuffle: np.random.shuffle(vectors)

		if algo=='MiniBatchKMeans':
			clusterer = MiniBatchKMeans(n_clusters = nb_clusters, verbose=verbose, max_no_improvement=max_no_improvement)
		if algo=='KMedoids':
			if metric is not None:
				clusterer = KMedoids(n_clusters=nb_clusters, max_iter=max_no_improvement, metric=metric)
			else:
				clusterer = KMedoids(n_clusters=nb_clusters, max_iter=max_no_improvement)
		clusterer.fit(vectors)

		if path_to_save is not None:
			np.save(path_to_save, clusterer.cluster_centers_)
		
		return clusterer
        
	@staticmethod
	def choose_number_clusters_clustering(vectors, algo, max_no_improvement, test_values ,figsize=(15, 5), verbose=0, metric=None):
        
		np.random.shuffle(vectors)
		distorsions = list()
		inertia = list()
		silhouette_scores = list()
		for k in test_values:
			model = Clusterer.fit_new_trainig(vectors, algo, nb_clusters=k, max_no_improvement=max_no_improvement, verbose=verbose, shuffle=False, metric=metric)
			labels = model.labels_
			inertia.append(model.inertia_)
			distorsions.append(metrics.calinski_harabasz_score(vectors, labels))
			silhouette_scores.append(metrics.silhouette_score(vectors, labels))
        
		Clusterer.draw_calinski_curve(test_values, distorsions, figsize)
		Clusterer.draw_elbow_curve(test_values, inertia, figsize)
		Clusterer.draw_silhoutte_curve(test_values, silhouette_scores, figsize)
        
	@staticmethod
	def draw_calinski_curve(x, y, figsize):
		fig = plt.figure(figsize=figsize)
		plt.plot(x, y, marker='o')
		plt.xticks(x)
		plt.xlabel('Number of clusters')
		plt.ylabel('Calinski harabaz score')
		plt.grid(True)
        
	@staticmethod
	def draw_elbow_curve(x, y, figsize):
		fig = plt.figure(figsize=figsize)
		plt.plot(x, y, marker='o')
		plt.xticks(x)
		plt.xlabel('Number of clusters')
		plt.ylabel('Within-cluster sum of squares')
		plt.grid(True)
		plt.title('Elbow curve')
        
	@staticmethod
	def draw_silhoutte_curve(x, y, figsize):
		fig = plt.figure(figsize=figsize)
		plt.plot(x, y, marker='o')
		plt.xticks(x)
		plt.xlabel('Number of clusters')
		plt.ylabel('Silhoutte Score')
		plt.grid(True)
		plt.title('Silhoutte curve')