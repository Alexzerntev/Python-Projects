import pandas as pd
import gmplot
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

def map_plot(traj,no,i,j):
     latitudes = [element[i] for element in traj]
     longitudes = [element[j] for element in traj]

     gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 13)
     gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width = 5)
     gmap.draw("mymap" + str(no) + ".html")

def double_map_plot(mapA, mapB, no):
     latitudesA = [element[1] for element in mapA]
     longitudesA = [element[0] for element in mapA]

     latitudesB = [element[1] for element in mapB]
     longitudesB = [element[0] for element in mapB]

     gmap = gmplot.GoogleMapPlotter(latitudesA[0], longitudesA[0], 13)
     gmap.plot(latitudesA, longitudesA, 'green', edge_width = 10)
     gmap.plot(latitudesB, longitudesB, 'red', edge_width = 10)
     gmap.draw("Neighbor" + no + ".html")

def block_map_plot(neighbor):
    no = 10
    for element in neighbor:     
        map_plot(element[2],no,1,0)
        no = no + 1

def write_predictions_to_csv(predictions):
    result = {
            "Test_Trip_ID":[],
            "Predicted_JourneyPatternID":[]
        }
    for x,y in predictions:
        result["Test_Trip_ID"].append(x)
        result["Predicted_JourneyPatternID"].append(y)
    data_frame = pd.DataFrame(result, columns= ['Test_Trip_ID', "Predicted_JourneyPatternID"])
    data_frame.to_csv("testSet_JourneyPatternIDs.csv", sep="\t", index = False, index_label = False)

def get_lat_lon(traj):
    for sublist in traj:
        del sublist[0]
    return np.array(traj)

def project_trajectories(trajectories):
    curent_index = 0
    result = []
    while curent_index < len(trajectories):
        current_traj = trajectories.get(curent_index)
        if current_traj == None:
            porjected_traj = current_traj
        else:
            porjected_traj = get_lat_lon(current_traj)
        result.append(porjected_traj)
        curent_index = curent_index + 1
    return result

# gets trajectories of type [[1,1] , [2,2], None, ..... ]
def remove_none(trajectories, input_ids):
    result = []
    output_ids = []
    for i,t in enumerate(trajectories):
        if t is not None:
            result.append(t)
            output_ids.append(input_ids[i])
    return result, output_ids

def findItem(List, Item):
   return [index for index in xrange(len(List)) if Item in List[index]]

def closest_neighbors(neighbor, id, traj, distance, number_of_neighbors):
    sublist = []
    if len(neighbor) < number_of_neighbors:
        sublist.append(id)
        sublist.append(distance)
        sublist.append(traj.tolist())
        neighbor.append(sublist)
    else:
        max_value = max(neighbor, key=lambda x: x[1])[1]
        max_index = findItem(neighbor,max_value)
        if distance < max_value:
            neighbor.pop(max_index[0])
            sublist.append(id)
            sublist.append(distance)
            sublist.append(traj.tolist())
            neighbor.append(sublist)
    return neighbor