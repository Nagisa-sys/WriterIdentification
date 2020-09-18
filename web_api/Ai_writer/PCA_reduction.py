import pickle
from sklearn.decomposition import PCA

class PCA_reduction:
	def __init__(self, pca_path):
		self.pca_reload = pickle.load(open(pca_path,'rb'))
	
	def reduce_size(self, vector):
		return self.pca_reload.transform([vector])[0]