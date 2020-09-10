import pickle
from sklearn.decomposition import PCA

class PCA_reduction:
	def __init__(self, pca_path):
		self.pca_reload = pickle.load(open(pca_path,'rb'))
	
	def reduce_size(self, vector):
		return self.pca_reload.transform([vector])[0]

	@staticmethod
	def create_new_pca_model(vectors, path_to_save="pca.pkl", n_components=300):
		pca = PCA(n_components=n_components)
		result = pca.fit(vectors)
		pickle.dump(pca, open(path_to_save,"wb"))