import pandas as pd
import numpy as np
import time
from ast import literal_eval
from fastdtw import fastdtw
from haversine import haversine
from helpers import *

trainSet = pd.read_csv('datasets/train_set.csv', converters={"Trajectory": literal_eval}, index_col='tripId')
testSet = pd.read_csv('datasets/test_set_a1.csv', sep="\t", converters={"Trajectory": literal_eval})

train_trajectory = trainSet['Trajectory']
train_journeyPatternId = trainSet['journeyPatternId']
train_trajectory.dropna(inplace=True)
test_trajectory = testSet['Trajectory']
test_trajectory.dropna(inplace=True)

current_index1 = 1
current_index2 = 0
limit = 0
while limit < len(test_trajectory):
    start = time.time()
    guard2 = test_trajectory.get(current_index2)
    while guard2 is None:
        current_index2 = current_index2 + 1
        guard2 = test_trajectory.get(current_index2)

    map_plot(guard2,limit+100,2,1)
    y = get_lat_lon(guard2)
    neighbor = []
    limit2 = 0
    current_index1 = 1
    while limit2 < len(train_trajectory):
        guard1 = train_trajectory.get(current_index1) 
        while guard1 is None:
            current_index1 = current_index1 + 1
            guard1 = train_trajectory.get(current_index1)

        if limit == 0:
            x = get_lat_lon(guard1)
        else:
            x = np.array(guard1)

        distance, path = fastdtw(x, y, dist=haversine)
        neighbor = closest_neighbors(neighbor,train_journeyPatternId.get(current_index1),x,distance,5)
        
        current_index1 = current_index1 + 1
        limit2 = limit2 + 1
    end = time.time()
    total_time = (end - start)
    print "time"
    print total_time
    print "---------------------------------------------------------"
    block_map_plot(neighbor)

    current_index2 = current_index2 + 1
    limit = limit + 1