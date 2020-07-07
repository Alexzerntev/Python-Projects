import pandas as pd
import gmplot
from haversine import haversine
from ast import literal_eval
from helpers import *
import time

def LCS(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if match(X[i - 1], Y[j - 1]): 
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i][j - 1], C[i - 1][j])
    return C, m ,n

def backTrack(C, X, Y, i, j):
    result = []
    if i == 0 or j == 0:
        return None
    elif match(X[i - 1], Y[j - 1]):
        bt = backTrack(C, X, Y, i - 1, j - 1)
        if bt is not None:
            result = result + bt
        result.append(X[i - 1])
        return result
    else:
        if C[i][j - 1] > C[i - 1][j]:
            bt = backTrack(C, X, Y, i, j - 1)
            return bt
        else:
            bt = backTrack(C, X, Y, i - 1, j)
            return bt

def match(X, Y):
    meter_dist = haversine(X, Y) * 1000
    if  meter_dist <= 200:
        return True
    return False

start = time.time()

trainSet = pd.read_csv('datasets/train_set.csv', converters={"Trajectory":literal_eval}, index_col='tripId')
testSet = pd.read_csv('datasets/test_set_a2.csv', sep="\t", converters={"Trajectory": literal_eval})

train_trajectories = trainSet['Trajectory']
JPIds = trainSet['journeyPatternId']
#train_trajectories = train_trajectories[0:100]

test_trajectories = testSet['Trajectory']
#test_trajectories = test_trajectories[0:100]


projected_train_traj = project_trajectories(train_trajectories)
projected_test_traj = project_trajectories(test_trajectories)

lcs_max_neighbours_per_test = []
times = []

for test_trajectory in projected_test_traj:
    start = time.time()
    lcs_max_neighbours = []
    if test_trajectory is None:
        continue
    for idx, train_trajectory in enumerate(projected_train_traj):
        if train_trajectory is None:
            continue
        array, m , n = LCS(test_trajectory, train_trajectory)
        if array[m][n] > 0:
            result = backTrack(array, test_trajectory, train_trajectory, m, n)
            if len(lcs_max_neighbours) < 5:
                lcs_max_neighbours.append([idx, result])
            else:
                min = lcs_max_neighbours[0]
                #finding min item
                for item in lcs_max_neighbours:
                    if len(item[1]) < len(min[1]):
                        min = item
                index = lcs_max_neighbours.index(min)
                if len(min[1]) < len(result):
                    lcs_max_neighbours[index] = [idx, result]
    lcs_max_neighbours.sort(key=lambda x: len(x[1]), reverse=True)
    lcs_max_neighbours_per_test.append(lcs_max_neighbours)
    end = time.time()
    total_time = (end - start)
    times.append(total_time)

for i,x in enumerate(lcs_max_neighbours_per_test):
    print "==============================================="
    for j,y in enumerate(x):
        print "-------------------"
        print "The the matching points are : "
        print len(y[1])
        print "Jp_id is : "
        print JPIds.get(y[0])
        print "Time is:"
        print times[i]
        print "Key is: "
        print str(i) + str(j)

        base_route = projected_train_traj[y[0]]
        common_route = y[1]
        key = str(i) + str(j)

        double_map_plot(base_route , common_route, key)


end = time.time()
print "Time ellapsed"
print(end - start)
print "Finish"
