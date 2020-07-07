import pandas as pd
import gmplot
from helpers import * 
from ast import literal_eval

trainSet = pd.read_csv('datasets/train_set.csv', converters={"Trajectory": literal_eval}, index_col='tripId')

trajectories = trainSet['Trajectory']
JPIds = trainSet['journeyPatternId']


used_JPId = []
current_index = 1
limit = 0

while limit < 5:
    if JPIds.iloc[current_index] not in used_JPId:
        guard = trajectories.get(current_index)
        if guard is None:
            current_index = current_index + 1
            continue
        
        map_plot(trajectories.get(current_index),limit,2,1)

        used_JPId.append(JPIds.iloc[current_index])
        limit = limit + 1
    current_index = current_index + 1