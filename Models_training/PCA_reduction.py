import pickle
from sklearn.decomposition import PCA
import numpy as np

class PCA_reduction:
	def __init__(self, pca_path):
		self.pca_reload = pickle.load(open(pca_path,'rb'))
	
	def reduce_size(self, vector):
		return self.pca_reload.transform([vector])[0]

	@staticmethod
	def create_new_pca_model(vectors, path_to_save, percentage_variance):
		from sklearn.preprocessing import MinMaxScaler
		scaler = MinMaxScaler()
		data_rescaled = scaler.fit_transform(vectors)

		pca = PCA(n_components=percentage_variance)
		result = pca.fit(data_rescaled)
		
		pickle.dump(pca, open(path_to_save,"wb"))

	@staticmethod
	def plot_variance_nbComponents(vectors, percentage_variance, figsize=(15, 5)):
		import matplotlib.pyplot as plt
		pca = PCA().fit(vectors)
		fig = plt.figure(figsize=figsize)
		plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o')
		plt.axhline(y=percentage_variance, color="red")
		plt.xlabel('No. of principal components')
		plt.ylabel('cumulative % variance retained')
		plt.grid(True)
		plt.title('Cumulative explained variance across the number of components ')