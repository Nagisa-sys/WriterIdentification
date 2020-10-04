from tensorflow.keras.models import load_model
import numpy as np
import cv2, pickle, math

class Encoder_NN:
	def __init__(self, shape_images, max_kp_treat_return, local_features_detector, verbose=True):
		self.local_features_detector = local_features_detector
		self.shape_images = shape_images
		self.max_kp_treat_return = max_kp_treat_return
		self.verbose = verbose


	def set_model(self, model_path):
		self.encoder = load_model(model_path, compile=False)


	def detectAndCompute(self, image, buffer):
		kps_cleaned = list()
		kps_cleaned_chosen = list()
		descriptors_cleaned = list()
		key_points = self.local_features_detector.detect(image,None)
		height = int(self.shape_images[0]/2)

		for key_point in key_points:
			if self.filter(image, key_point):
				kps_cleaned.append(key_point)

		kps_cleaned_chosen = self.less_key_points(kps_cleaned, min_distance=height*2, min_angle = 0.25, max_len_return=self.max_kp_treat_return)
		
		for key_point in kps_cleaned_chosen:
			y,x = int(key_point.pt[0]),int(key_point.pt[1])
			descriptors_cleaned.append(self.encode_part(image, x, y, height))
		
		return kps_cleaned_chosen, descriptors_cleaned


	def less_key_points(self, kps_cleaned_chosen, min_distance, min_angle, max_len_return):
		def distance_center(point):
  			return math.sqrt(point.pt[0]**2 + point.pt[1]**2)
		
		key_points_distance = np.array(sorted(kps_cleaned_chosen, key=lambda x: distance_center(x)))
		i = 0
		if self.verbose : 
		    print("treated ", self.max_kp_treat_return, "/", len(key_points_distance), " key points !", sep = '')
		while True:
			if i+1 >= len(key_points_distance):
				break
			if distance_center(key_points_distance[i]) + min_distance >= distance_center(key_points_distance[i+1]) :
				u = np.array([key_points_distance[i].pt[1], key_points_distance[i].pt[0]])
				v = np.array([key_points_distance[i+1].pt[1], key_points_distance[i+1].pt[0]])
				c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)
				angle = np.arccos(np.clip(c, -1, 1))
				if (-min_angle < angle < min_angle):
					key_points_distance = np.delete(key_points_distance, i+1)
					i -= 1
			i +=1
		
		return key_points_distance[np.random.choice(key_points_distance.shape[0], min(max_len_return,len(key_points_distance)), replace=False)]


	def encode_part(self, image, x, y, height):
		cropped = image[x-height:x+height,y-height:y+height]
		cropped = np.array( [cropped,])
		cropped = np.expand_dims(cropped, axis=-1)
		cropped = cropped.astype("float32") / 255.0
		return self.encoder.predict(cropped)[0]


	def filter(self, image, key_point):
		y,x = int(key_point.pt[0]),int(key_point.pt[1])
		s = int(key_point.size/2)
		Sn = np.sum(image[y-s:y+s,x-s:x+s]==0)
		if (Sn >= (s-1)):
			xm, ym = image.shape
			height = int(self.shape_images[0]/2)
			if not ((x-height < 0) or (x+height > xm) or (y-height < 0) or (y+height > ym)):
				return True
		return False