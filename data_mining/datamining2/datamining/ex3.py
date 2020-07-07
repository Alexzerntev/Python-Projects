import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from helpers import *
from Knn import *
from ast import literal_eval


trainSet = pd.read_csv('datasets/train_set.csv', converters={"Trajectory":literal_eval}, index_col='tripId')
testSet = pd.read_csv('datasets/test_set_a2.csv', sep="\t", converters={"Trajectory": literal_eval})

train_trajectories = trainSet['Trajectory']
#train_trajectories = train_trajectories[0:100]

test_trajectories = testSet['Trajectory']
#test_trajectories = test_trajectories[0:100]

JPIds = trainSet['journeyPatternId']
#JPIds = JPIds[0:100]

# Building encoder and transforming categories
labelEncoder = preprocessing.LabelEncoder()
y = labelEncoder.fit(JPIds).transform(JPIds)

#projecting data
X = project_trajectories(train_trajectories)
T = project_trajectories(test_trajectories)

X, y = remove_none(X, y)

KNN_classifier = KNearestNeighbor()
KNN_classifier.fit(X, y)

predicted = KNN_classifier.predict(T)
predicted_journeys = labelEncoder.inverse_transform(predicted)

ids = [1,2,3,4,5]
result = zip(ids, predicted_journeys)
write_predictions_to_csv(result)

sample = int(len(X)* 0.05)
print "Sample is: "
print sample
X = X[0 : sample]
y = y[0 : sample]

accuracy = cross_val_score(KNN_classifier, X, y, cv=10, scoring = 'accuracy')
print("Accuracy: %0.2f (+/- %0.2f)" % (accuracy.mean(), accuracy.std() * 2))