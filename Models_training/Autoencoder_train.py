from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Conv2DTranspose
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Reshape
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Lambda
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam

import matplotlib.pyplot as plt
import numpy as np
import pickle
from functools import reduce

class Autoencoder_train:
	def __init__(self, configuration, data_path, model_path):
		self.configuration = configuration
		self.shape_images = (configuration["shape_images"]*2,configuration["shape_images"]*2)
		self.model_path = model_path
		self.data_path = data_path
        
        
	@staticmethod
	def prepare_vectors(vectors):
	# add a channel dimension to every image in the dataset, then scale
	# the pixel intensities to the range [0, 1]
		vectors = np.expand_dims(vectors, axis=-1)
		vectors = vectors.astype("float32") / 255.0
		return vectors
    
    
	def train_network(self):
		test_ration = self.configuration["autoencoder_test_ration"]
		EPOCHS = self.configuration["EPOCHS"]
		BS = self.configuration["BS"]

		trainX, testX = self.load_data_patchs(self.data_path, test_ration)

		trainX 	= Autoencoder_train.prepare_vectors(trainX)
		testX 	= Autoencoder_train.prepare_vectors(testX)

	# construct the convolutional autoencoder
		print("[INFO] building autoencoder...")
		(encoder, decoder, autoencoder) = self.build(self.shape_images[0], self.shape_images[1], 1)
		self.autoencoder=autoencoder
		autoencoder.compile(loss="mse", optimizer=Adam(lr=1e-3))

	# train the convolutional autoencoder
		history = autoencoder.fit(trainX, trainX,
								validation_data=(testX, testX),
								epochs=EPOCHS,
								batch_size=BS)

		self.plot_loss_accuracy(history, EPOCHS)
		print("*"*10)
		print("last value of cost function:",history.history["val_loss"][-1])
		print("*"*10)
		self.encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer("encoder").output)
		self.save_model(encoder, self.model_path)
		self.visualize_predictions(autoencoder, testX)
		return history.history["val_loss"][-1]

	def visualize_predictions(self, autoencoder, testX, samples=20):
		print("[INFO] making predictions...")
		decoded = autoencoder.predict(testX)
		outputs = None
		for i in range(0, samples):
			original = (testX[i] * 255).astype("float32")
			recon = (decoded[i] * 255).astype("float32")
			output = np.hstack([original, recon])
			if outputs is None:
				outputs = output
			else:
				outputs = np.vstack([outputs, output])
		plt.figure(figsize=(30,30))
		plt.imshow(outputs[:,:,0], cmap='gray')
		plt.axis('off')
		plt.show()

	def load_data_patchs(self, PIK, test_ration):
		with open(PIK,'rb') as f:
			data = np.array(pickle.load(f))

		size_test = int(len(data)*test_ration)
		#np.random.shuffle(data)
		return data[size_test:], data[:size_test]


	def save_model(self, model, model_path):
		save_format = "h5"
		print("[INFO] saving encoder...")
		model.save(model_path, save_format=save_format, include_optimizer=False)


	def plot_loss_accuracy(self, H, EPOCHS):
		N = np.arange(0, EPOCHS)
		plt.style.use("ggplot")
		plt.figure()
		plt.plot(N, H.history["loss"], label="train_loss")
		plt.plot(N, H.history["val_loss"], label="val_loss")
		plt.title("Training Loss and Accuracy")
		plt.xlabel("Epoch #")
		plt.ylabel("Loss/Accuracy")
		plt.legend(loc="lower left")


	
	def build(self, width, height, depth, filters=(32, 64)):
		latentDim = self.configuration["latentDim"]
		inputShape = (height, width, depth)

		inputs = Input(shape=inputShape)
		x = inputs

		for f in filters:
			x = Conv2D(f, (3, 3), strides=2, padding="same")(x)
			x = LeakyReLU(alpha=0.2)(x)
			x = BatchNormalization()(x)

		volumeSize = K.int_shape(x)
		x = Flatten()(x)
		latent = Dense(latentDim)(x)
		def custom_layer(tensor):
			return K.l2_normalize(tensor,axis=1)
		latent_normalised = Lambda(custom_layer, name="lambda_l2_layer")(latent)
		encoder = Model(inputs, latent_normalised, name="encoder")
		print(encoder.summary())

		latentInputs = Input(shape=(latentDim,))
		x = Dense(np.prod(volumeSize[1:]))(latentInputs)
		x = Reshape((volumeSize[1], volumeSize[2], volumeSize[3]))(x)

		for f in filters[::-1]:
			x = Conv2DTranspose(f, (3, 3), strides=2, padding="same")(x)
			x = LeakyReLU(alpha=0.2)(x)
			x = BatchNormalization()(x)

		x = Conv2DTranspose(depth, (3, 3), padding="same")(x)
		outputs = Activation("sigmoid")(x)
		decoder = Model(latentInputs, outputs, name="decoder")

		autoencoder = Model(inputs, decoder(encoder(inputs)), name="autoencoder")
		return (encoder, decoder, autoencoder)

	@staticmethod
	def generate_patchs(PatchsPickle, local_features_extractor, images, height, max_samples_by_image):
		images_patchs = list()
		i=0
		for image in images:
			key_points = local_features_extractor.kps(image)
			retained_patches = list()
			for key_point in key_points:
				y,x = int(key_point.pt[0]),int(key_point.pt[1])
				xm, ym = len(image[0]), len(image)
				cropped = image[x-height:x+height,y-height:y+height]
				if reduce(lambda x, y: x*y, np.shape(cropped))!=height*height*4: continue
				retained_patches.append(cropped)
			retained_patches = np.array(retained_patches)
			images_patchs.extend(retained_patches[np.random.choice(retained_patches.shape[0], min(max_samples_by_image,len(retained_patches)), replace=False)])
			i+=1
			if i%100==0: print("100 images treated")
		with open(PatchsPickle, "wb") as f:
			pickle.dump(list(images_patchs), f)