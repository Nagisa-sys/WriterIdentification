import numpy as np
from scipy.cluster.vq import vq
from Norms import Norm


class VLAD :
	def __init__ (self, clusters_centers, pca_instance=None):
		self.clusters_centers = clusters_centers
		self.pca_instance = pca_instance

	def global_feature_vector (self, descriptors):
		dimensions = descriptors[0].shape[0]
		vlad_vector = np.zeros((len(self.clusters_centers), dimensions), dtype=np.float32)

		center_idx, _ = vq(descriptors, self.clusters_centers)
		for i, idx in enumerate(center_idx):
			vlad_vector[idx] += (descriptors[i] - self.clusters_centers[idx])

		Norm.intra_normalization(vlad_vector)

		vlad_vector = vlad_vector.flatten()

		Norm.l2_normalization(vlad_vector)

		if self.pca_instance is None :
			return vlad_vector
			
		vlad_pca_vector = self.pca_instance.reduce_size(vlad_vector)

		return vlad_pca_vector


class BOW :
	def __init__ (self, clusters_centers):
		self.clusters_centers = clusters_centers
	
	def global_feature_vector (self, descriptors):
		histogram = np.zeros(len(self.clusters_centers))

		center_idx, _ = vq(descriptors, self.clusters_centers)

		for idx in center_idx:
			histogram[idx] += 1
		
		Norm.l1_normalization(histogram)

		return histogram