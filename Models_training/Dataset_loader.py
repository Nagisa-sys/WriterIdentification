import os
import numpy as np
from itertools import islice
from collections import Counter
import random

def Load_IAM_form_writer(WORK_DIR):
  forms_IAM_base_path = WORK_DIR+"/dataset/IAM"
  form_writer = {}
  forms_file_path = forms_IAM_base_path+"/forms_IAM.txt"
  with open(forms_file_path) as f:
    for line in islice(f, 16, None):
      line_list = line.split(' ')
      form_id = line_list[0]
      writer = "IAM_"+line_list[1]
      form_writer[forms_IAM_base_path+"/"+form_id+".png"] = writer
  return form_writer

def Load_TS_form_writer(WORK_DIR):
  forms_TS_base_path = WORK_DIR+"/dataset/TrigraphSlant"
  form_writer = {}
  for filename in os.listdir(forms_TS_base_path):
    file_w_ext = os.path.splitext(filename)[0]
    form_writer[forms_TS_base_path+"/"+file_w_ext+".png"] = "TS_" + file_w_ext[:4]
  return form_writer

def Load_ICDAR2013_form_writer(WORK_DIR):
  forms_TS_base_path = WORK_DIR+"/dataset/ICDAR2013"
  form_writer = {}
  for filename in os.listdir(forms_TS_base_path):
    file_w_ext = os.path.splitext(filename)[0]
    form_writer[forms_TS_base_path+"/"+file_w_ext+".jpg"] = "ICDAR_" + file_w_ext[:4]
  return form_writer

def filter_form_writer(form_writer):
  min_forms = 2
  writers_counter = Counter(form_writer.values())
  top_writers_ = [id for id in writers_counter if writers_counter[id] >= min_forms]
  top_writers = []
  top_forms = []
  for form_id, author_id in form_writer.items():
    if author_id in top_writers_:
      top_forms.append(form_id)
      top_writers.append(author_id)

  return top_writers, top_forms

def load_dataset(form_writer):
  writers, images = filter_form_writer (form_writer)
  writers, images = np.array(writers), np.array(images)
  indices = random.sample(range(writers.shape[0]), writers.shape[0])
  writers, images = writers[indices], images[indices]
  return writers, images
	
def load_dataset_all(WORK_DIR):
	form_writer = {**Load_IAM_form_writer(WORK_DIR),
                  **Load_TS_form_writer(WORK_DIR),
                   **Load_ICDAR2013_form_writer(WORK_DIR)}
	return load_dataset(form_writer)

def load_dataset_ICDAR(WORK_DIR):
  form_writer = Load_ICDAR2013_form_writer(WORK_DIR)
  return load_dataset(form_writer)

def load_dataset_IAM(WORK_DIR):
  form_writer = Load_IAM_form_writer(WORK_DIR)
  return load_dataset(form_writer)