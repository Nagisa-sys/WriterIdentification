from . import Local_features_extractor, Global_feature_exractors
from . import Autoencoder, PCA_reduction
from . import Clusterer, Distances, Norms
from . import Image
import numpy as np
import json

#Sift_Descr_Vlad_Pca : SDVP
#Sift_Encoder_Vlad_Pca : SEVP
#Sift_Desc_Bow : SDB


class Writer_identification:
	def __init__(self, configuration_file="config_algo.json"):
		with open(configuration_file) as config_file:
			configuration_all = json.load(config_file)
		self.SDVP = self.prepareSDVP(configuration_all["Sift_Vlad_Pca"])
		self.SDB = self.prepareSDB(configuration_all["Sift_Bow"])
		self.SEVP = self.prepareSEVP(configuration_all["Sift_Encoder_Vlad_Pca"])


	def prepareSDVP(self, config):
		pca_path = config["path_pca_model"]
		cluster_centers_path = config["path_cluster_centers"]

		hellinger_normalization = Norms.Norm.hellinger_normalization
		local_features_extractor = Local_features_extractor.Local_feature_exractor(hellinger_normalization)
		
		pca_instance = PCA_reduction.PCA_reduction(pca_path)
		clusters_centers = Clusterer.clusterer.fit_ancient_data(cluster_centers_path)
		vlad = Global_feature_exractors.VLAD(clusters_centers, pca_instance=pca_instance)
		chi2_distance = Distances.Distance.chi2_distance

		return (local_features_extractor, vlad, chi2_distance)


	def prepareSDB(self, config):
		cluster_centers_path = config["path_cluster_centers"]

		hellinger_normalization = Norms.Norm.hellinger_normalization
		local_features_extractor = Local_features_extractor.Local_feature_exractor(hellinger_normalization)
		
		clusters_centers = Clusterer.clusterer.fit_ancient_data(cluster_centers_path)
		bow = Global_feature_exractors.BOW(clusters_centers)
		
		chi2_distance = Distances.Distance.chi2_distance

		return (local_features_extractor, bow, chi2_distance)


	def prepareSEVP(self, config):
		pca_path = config["path_pca_model"]
		cluster_centers_path = config["path_cluster_centers"]
		shape_images = config["shape_images"]*2
		max_key_points = config["max_key_points"]
		model_path = config["model_path"]

		autoencoder = Autoencoder.Encoder_NN((shape_images, shape_images), max_key_points)
		autoencoder.set_model(model_path=model_path)
		local_features_extractor = Local_features_extractor.Local_feature_exractor(Norms.Norm.No_norm, local_feature_extractor=autoencoder)

		clusters_centers = Clusterer.clusterer.fit_ancient_data(cluster_centers_path)
		pca_instance = PCA_reduction.PCA_reduction(pca_path)
		vlad = Global_feature_exractors.VLAD(clusters_centers, pca_instance=pca_instance)

		cosine_distance = Distances.Distance.cosine_distance

		return (local_features_extractor, vlad, cosine_distance)


	def predict(self, methode, images, writers, target_image):
		if methode == "SDVP" :
			local_features_extractor, global_feature_extractor, distance_metric = self.SDVP
		if methode == "SDB" :
			local_features_extractor, global_feature_extractor, distance_metric = self.SDB
		if methode == "SEVP" :
			local_features_extractor, global_feature_extractor, distance_metric = self.SEVP

		images_pre = [Image.Image(path_image, local_features_extractor, global_feature_extractor=global_feature_extractor, url=True) for path_image in images]
		target_pre = Image.Image(target_image, local_features_extractor, global_feature_extractor=global_feature_extractor, url=True)

		distances = list()
		for i in range(len(images_pre)):
			distances.append(distance_metric(images_pre[i].global_descriptor,target_pre.global_descriptor))

		return writers[np.argmin(distances)]
