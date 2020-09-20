import os, cv2
from itertools import islice
import numpy as np

def Load_dataset_IAM(IAM_base_path):
  writers, images = [], []
  forms_file_path = IAM_base_path+"/forms_IAM.txt"
  with open(forms_file_path) as f:
    for line in islice(f, 16, None):
      line_list = line.split(' ')
      form_id = line_list[0]
      writers.append("IAM_"+line_list[1])
      images.append(IAM_base_path+"/"+form_id+".png")
  return writers, images


def Load_dataset_ICDAR2013(TS_base_path, language='en'):
  assert language in ["all", "en", "ar"]
  writers, images = [], []
  #the if outside the loop is better computationally than the other way around
  if language=='all':
    for filename in os.listdir(TS_base_path):
      file_w_ext = os.path.splitext(filename)[0]
      writers.append("ICDAR2013_" + file_w_ext[:4])
      images.append(TS_base_path+"/"+file_w_ext+".jpg")
  else:
    if language=='en': ext = ("_3.jpg", "_4.jpg")
    if language=='ar': ext = ("_1.jpg", "_2.jpg")
    for filename in os.listdir(TS_base_path):
      file_w_ext = os.path.splitext(filename)[0]
      if not filename.endswith(ext) : continue
      writers.append("ICDAR2013_" + file_w_ext[:4])
      images.append(TS_base_path+"/"+file_w_ext+".jpg")
  
  return writers, images


def Load_dataset_TrigraphSlant(TS_base_path, slant=False):
  writers, images = [], []
  if slant : ext = ("l.png", "r.png")
  else : ext = ("n.png")

  for filename in os.listdir(TS_base_path):
    if not filename.endswith(ext) : continue
    file_w_ext = os.path.splitext(filename)[0]
    writers.append("TS_" + file_w_ext[:4])
    images.append(TS_base_path+"/"+file_w_ext+".png")
  
  return writers, images


def train_test_IAM(WORK_DIR, size_train, size_test):
  def image_preprocessing(image_path):
    return cv2.cvtColor(cv2.imread(image_path),cv2.COLOR_BGR2GRAY)[700:2700,40:-40]
    
  writers, images = Load_dataset_IAM(WORK_DIR)
  writers = np.array(writers)
  unique_writers = np.unique(writers)
  W_test, I_test_p, W_train, I_train_p = [], [], [], []

  for writer in unique_writers:
    indices = np.nonzero(writers == writer)[0][0:2]
    if len(indices)<2 : continue
    W_test.extend([writer, writer])
    I_test_p.extend([images[indices[1]], images[indices[0]]])
    if len(W_test)>size_test: break

  for i in range(len(images)):
    image = images[i]
    if image not in I_test_p:
      I_train_p.append(image)
      W_train.append(writers[i])
    if len(W_train)==size_train: break

  print("Training set:", len(I_train_p))
  print("Testing set:", len(I_test_p))

  I_test = [image_preprocessing(image_path) for image_path in I_test_p]
  I_train = [image_preprocessing(image_path) for image_path in I_train_p]
  I_train_names = ["IAM_"+os.path.splitext(os.path.basename(path))[0] for path in I_train_p]
  I_test_names = ["IAM_"+os.path.splitext(os.path.basename(path))[0] for path in I_test_p]

  return list(zip(W_train, I_train_names, I_train)), list(zip(W_test, I_test_names, I_test))


def train_test_ICDAR2013(WORK_DIR, size_train, size_test, language='en'):
  def image_preprocessing(image_path):
    return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)

  W_train, I_train_p = Load_dataset_ICDAR2013(WORK_DIR+"/train", language)
  print("Train set : from",len(W_train),end="")
  W_train, I_train_p = W_train[: min(size_train,len(W_train))], I_train_p[: min(size_train,len(I_train_p))]
  print(",", len(W_train), "fetched.")

  W_test, I_test_p = Load_dataset_ICDAR2013(WORK_DIR+"/test", language)
  print("Test set : from",len(W_test),end="")
  W_test, I_test_p = W_test[: min(size_test,len(W_test))], I_test_p[: min(size_test,len(I_test_p))]
  print(",", len(W_test), "fetched.")

  I_test = [image_preprocessing(image_path) for image_path in I_test_p]
  I_train = [image_preprocessing(image_path) for image_path in I_train_p]
  I_train_names = ["ICDAR2013_"+os.path.splitext(os.path.basename(path))[0] for path in I_train_p]
  I_test_names = ["ICDAR2013_"+os.path.splitext(os.path.basename(path))[0] for path in I_test_p]

  return list(zip(W_train, I_train_names, I_train)), list(zip(W_test, I_test_names, I_test))


def train_test_TrigraphSlant(WORK_DIR, size_train, size_test, slant=False):
  def image_preprocessing(image_path):
    return cv2.cvtColor(cv2.imread(image_path),cv2.COLOR_BGR2GRAY)[600:,:]

  W_train, I_train_p = Load_dataset_TrigraphSlant(WORK_DIR+"/train", slant)
  print("Train set : from",len(W_train),end="")
  W_train, I_train_p = W_train[:min(size_train,len(W_train))], I_train_p[:min(size_train,len(I_train_p))]
  print(",", len(W_train), "fetched.")

  W_test, I_test_p = Load_dataset_TrigraphSlant(WORK_DIR+"/test", slant)
  print("Test set : from",len(W_test),end="")
  W_test, I_test_p = W_test[:min(size_test,len(W_test))], I_test_p[:min(size_test,len(I_test_p))]
  print(",", len(W_test), "fetched.")  

  I_test = [image_preprocessing(image_path) for image_path in I_test_p]
  I_train = [image_preprocessing(image_path) for image_path in I_train_p]
  I_train_names = ["TrigraphSlant_"+os.path.splitext(os.path.basename(path))[0] for path in I_train_p]
  I_test_names = ["TrigraphSlant_"+os.path.splitext(os.path.basename(path))[0] for path in I_test_p]

  return list(zip(W_train, I_train_names, I_train)), list(zip(W_test, I_test_names, I_test))
