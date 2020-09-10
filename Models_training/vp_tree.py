import numpy as np
from random import randrange
from collections import deque

class PriorityQueue(object):
    def __init__(self, size=None):
        self.queue = []
        self.size = size

    def push(self, priority, item):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda x: x[0])
        if self.size is not None and len(self.queue) > self.size:
            self.queue.pop()


class VPTree(object):

    def __init__(self, points, dist_fn):
        self.left = None
        self.right = None
        self.median = None
        self.dist_fn = dist_fn
        self.build_tree(points)

    def build_tree(self, points):
        # vantage point is randomly chosen
        self.vp = points.pop(randrange(len(points)))
        if len(points) < 1:
            return

        # split in half by distances's median
        distances = [self.dist_fn(self.vp, p) for p in points]
        self.median = np.median(distances)

        left_points = []
        right_points = []
        for point, distance in zip(points, distances):
            if distance >= self.median:
                right_points.append(point)
            else:
                left_points.append(point)

        if len(left_points) > 0:
            self.left = VPTree(points=left_points, dist_fn=self.dist_fn)

        if len(right_points) > 0:
            self.right = VPTree(points=right_points, dist_fn=self.dist_fn)


    def is_leaf(self):
        return (self.left is None) and (self.right is None)

    def find_neighbors(self, point, k):
        neighbors = PriorityQueue(k)
        self._find_neighbors(point, k, self, neighbors)
        return neighbors.queue

    def _find_neighbors(self, point, k, node, neighbors):
        if node == None : return 

        distance = self.dist_fn(node.vp, point)
        neighbors.push(distance, node.vp)

        tau, _ = neighbors.queue[-1]

        if node.is_leaf() : return

        if distance < node.median : 
            if distance <= (node.median + tau) : self._find_neighbors(point, k, node.left, neighbors)
            if distance >= (node.median - tau) : self._find_neighbors(point, k, node.right, neighbors)
        else : 
            if distance >= (node.median - tau) : self._find_neighbors(point, k, node.right, neighbors)
            if distance <= (node.median + tau) : self._find_neighbors(point, k, node.left, neighbors)