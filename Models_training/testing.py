from random import shuffle
import numpy as np
from sklearn.neighbors import BallTree
import vp_tree, os
from multiprocessing import Pool
from itertools import repeat


def accuracy(X_test, y_test, global_feature_extractor, distance_metric):
	#[image.set_global_descriptor(global_feature_extractor) for image in X_test if not image.has_global_descriptor()]
	incorrect, correct = 0, 0
	for i in range(len(X_test)):
		distances = list()
		for j in range(len(X_test)):
			distances.append(distance_metric(X_test[i].global_descriptor, X_test[j].global_descriptor))
		distances[i] = np.inf
		current_prediction = y_test[np.argmin(distances)]
		current_prediction_image_name = X_test[np.argmin(distances)].name
		print(y_test[i]," ==> ",current_prediction,"(",X_test[i].name,",",current_prediction_image_name,")")
		if y_test[i] == current_prediction: correct+=1
		else : incorrect += 1
	return correct/(correct+incorrect)

def accuracy_vp_tree(X_test, y_test, global_feature_extractor, distance_metric):
	def distance_for_tree(elementA, elementB):
		return distance_metric(elementA.global_descriptor, elementB.global_descriptor)

	[setattr(X_test_e, "author", y_test_e)  for (X_test_e, y_test_e) in zip(X_test, y_test)]
	correct = 0

	tree = vp_tree.VPTree(np.copy(X_test).tolist(), dist_fn=distance_for_tree)
	for i in range(len(X_test)):
		result = tree.find_neighbors(X_test[i], 2)[1][1]
		print(X_test[i].author," ==> ",result.author,"(",X_test[i].name,",",result.name,")")
		if result.author == X_test[i].author : correct += 1

	return correct/len(X_test)

def tree_search(global_descriptor, index, tree, authors, images_names, past_results):
	result_ind = past_results.get(index)
	if not result_ind:
		_, result = tree.query(global_descriptor.reshape(1, -1), k=2)
		result_ind = result[0][1]
		past_results[result_ind] = index
	print(authors[index]," ==> ",authors[result_ind],"(",images_names[index],",",images_names[result_ind],")")
	if authors[index] == authors[result_ind] :  return 1
	return 0


def accuracy_optimised(X_test, y_test, global_feature_extractor, distance_metric):
	[setattr(X_test_e, "author", y_test_e)  for (X_test_e, y_test_e) in zip(X_test, y_test)]

	distances = []
	[distances.append(image.global_descriptor) for image in X_test]
	distances = np.array(distances)
	indices = list(range(len(distances)))

	tree = BallTree(distances, leaf_size=2, metric=distance_metric)

	pool = Pool(os.cpu_count())
	past_results = {}
	images_names = []
	[images_names.append(image.name) for image in X_test]
	images_names = np.array(images_names)              
	results = pool.starmap(tree_search, zip(distances, indices, 
											repeat(tree), repeat(y_test), repeat(images_names), repeat(past_results)))

	return sum(results)/len(X_test)



def get_test_sample(images, writers, nb_to_use):

	X_test, y_test = np.array([]), np.array([])
	unique_writers = np.unique(writers)

	number_writers_test = min(int(nb_to_use/2), len(unique_writers))
	random_base = list(range(len(unique_writers)))
	shuffle(random_base)


	for i in range(number_writers_test):
		writer = unique_writers[random_base[i]]

		indices = np.nonzero(writers == writer)[0][0:2]

		y_test = np.append(y_test, (writer, writer))
		X_test = np.append(X_test, (images[indices[1]], images[indices[0]]))


	random_base = list(range(len(X_test)))
	shuffle(random_base)
	X_test = X_test[random_base]
	y_test = y_test[random_base]

	return X_test, y_test