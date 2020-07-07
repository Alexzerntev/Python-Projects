from operator import itemgetter
from collections import Counter

import numpy as np
import math


 
class KNearestNeighbor:

    def __init__(self, X = None, y = None, train = None, k = 5):
        self.k = k
        self.X = X
        self.y = y
        self.train = train


    # calculates the distance between 2 vectors
    def get_distance(self, data1, data2):
        distance = 0 
        for idx, val in enumerate(data1):
            distance += pow(data1[idx] - data2[idx], 2)
        return math.sqrt(distance)
 
    # getting neighbours
    def get_neighbours(self, training_set, test_instance):
        distances = [self.get_tuple_distance(training_instance, test_instance) for training_instance in training_set]
        sorted_distances = sorted(distances, key = itemgetter(1))
        sorted_training_instances = [tuple[0] for tuple in sorted_distances]
        return sorted_training_instances[:self.k]


    # private method to convert to tuple instance and its distance 
    def get_tuple_distance(self, training_instance, test_instance):
        return (training_instance, self.get_distance(test_instance, training_instance[0]))
 
    # getting majority vote (selects category with the most votes)
    def get_majority_vote(self, neighbours):
        categories = [neighbour[1] for neighbour in neighbours]
        count = Counter(categories)
        return count.most_common()[0][0] 

    # predicting for T based on X
    def predict(self, T):
        predictions = []
        for x in range(len(T)):
            neighbours = self.get_neighbours(training_set=self.train, test_instance=T[x])
            majority_vote = self.get_majority_vote(neighbours)
            predictions.append(majority_vote)
        return predictions


    def fit(self, X, y):
        self.X = X
        self.y = y
        self.train = np.array(zip(X, y))

    def get_params(self, deep=True):
        return {"X": self.X, "y": self.y, "train":self.train, "k": self.k}
        
