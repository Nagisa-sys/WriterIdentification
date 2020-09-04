import numpy as np
import math

class Norm:

  @staticmethod
  def hellinger_normalization(vector):
    vector += np.finfo(np.float32).eps
    vector /= np.sum(vector, axis=1)[:, np.newaxis]
    vector = np.sqrt(vector)
    return vector

  @staticmethod
  def No_norm(vector):
    return vector

  @staticmethod
  def intra_normalization(vector):
    for element in vector :
      element = element / max(np.linalg.norm(element, ord=2), +1e-9)

  @staticmethod
  def l2_normalization(vector):
    norme = max(math.sqrt(np.sum(vector * vector)), 1e-12)
    vector /= norme

  @staticmethod
  def l1_normalization(vector):
    vector = vector/np.sum(vector)