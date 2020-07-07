import pandas as pd
import gmplot
from haversine import haversine
from ast import literal_eval
from helpers import *
import time

testSet = pd.read_csv('datasets/test_set_a2.csv', sep="\t", converters={"Trajectory": literal_eval})
test_trajectories = testSet['Trajectory']
projected_test_traj = project_trajectories(test_trajectories)



for i,x in enumerate(projected_test_traj):
    latitudes = [element[1] for element in x]
    longitudes = [element[0] for element in x]
    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 13)
    gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width = 15)
    gmap.draw("test" + str(i) + ".html")

