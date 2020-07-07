import pandas as pd

from KNearestNeighbor import KNearestNeighbor
from BeatTheBenchmark import BeatTheBenchmark

from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import cross_val_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from Helpers import *
from Plots import make_plots_for_classifier

def get_metrics(classifier, X, y):

    accuracy = cross_val_score(classifier, X, y, cv=10, scoring = 'accuracy')
    f1 = cross_val_score(classifier, X, y, cv=10, scoring='f1_macro')
    precision = cross_val_score(classifier, X, y, cv=10, scoring='precision_macro')
    recall = cross_val_score(classifier, X, y, cv=10, scoring='recall_macro')

    print ""
    print("Precision: %0.2f (+/- %0.2f)" % (precision.mean(), precision.std() * 2))
    print("Recall: %0.2f (+/- %0.2f)" % (recall.mean(), recall.std() * 2))
    print("Accuracy: %0.2f (+/- %0.2f)" % (accuracy.mean(), accuracy.std() * 2))
    print("F-Measure: %0.2f (+/- %0.2f)" % (f1.mean(), f1.std() * 2))

    return [accuracy.mean(), precision.mean(), recall.mean(), f1.mean()]


train_data = pd.read_csv("DataSets/stemmed_train_set.csv", sep="\t")
#train_data = train_data[0:200]


test_data = pd.read_csv("DataSets/stemmed_test_set.csv", sep = "\t")
#test_data = test_data[0:200]


categories = train_data['Category']
title_weight = 2
# getting contntent with 'weight' time the title
#for idx, row in train_data.iterrows():
#    current_content = row.Content
#    if current_content != current_content:
#        current_content = ""
#    current_title = row.Title
#    for i in range(title_weight): # here goes the wight of title
#        current_content = current_content + " " + current_title
#    train_data.set_value(idx, 'Content', current_content)

train_contents = train_data['Content']

# seperating test dataset
#for idx, row in test_data.iterrows():
#    current_content = row.Content
#    if current_content != current_content:
#        current_content = ""
#    current_title = row.Title
#    for i in range(title_weight): # here goes the wight of title
#        current_content = current_content + " " + current_title
#    test_data.set_value(idx, 'Content', current_content)

test_contents = test_data['Content']

# vectorizing data
vectorized_train_data = TfidfVectorizer(stop_words = 'english').fit_transform(train_contents)
vectorized_test_data = TfidfVectorizer(stop_words = 'english').fit_transform(test_contents)
# performing LSI
X = TruncatedSVD(n_components = 40).fit_transform(vectorized_train_data)
T = TruncatedSVD(n_components = 40).fit_transform(vectorized_test_data)


# Building encoder and transforming categories
#labelEncoder = preprocessing.LabelEncoder()
#y = labelEncoder.fit(categories).transform(categories)

# Support Vector Machines 
#result = svc_param_selection(X, y, 3)
#SVM_classifier = svm.SVC(C=result['C'], kernel=result['kernel'],gamma=result['gamma'],decision_function_shape='ovo')
#SVM_classifier.fit(X, y)

#predicted = SVM_classifier.predict(T)
#predicted_categories = labelEncoder.inverse_transform(predicted) # to write to file

# Random forests
#RF_classifier = RandomForestClassifier()
#RF_classifier.fit(X, y)

#predicted = RF_classifier.predict(T)
#predicted_categories = labelEncoder.inverse_transform(predicted) # to write to file

# Naive Bayes
#NB_classifier = GaussianNB()
#NB_classifier.fit(X, y)

#predicted = NB_classifier.predict(T)
#predicted_categories = labelEncoder.inverse_transform(predicted) # to write to file

#KNN_classifier = KNearestNeighbor()
#KNN_classifier.fit(X, y)

#predictions = KNN_classifier.predict(T)

BM_classifier = BeatTheBenchmark(X,y)
BM_classifier.fit(X,y)
predicted = BM_classifier.predict(T)
predicted_categories = labelEncoder.inverse_transform(predicted)

#predicted = SVM_classifier.predict(T)
#predicted_categories = labelEncoder.inverse_transform(predicted)

result1 = zip(test_data['Id'],predicted_categories)

#col = ["Accuracy", "Precision", "Recall", "F-Measure"]
#bm_metrics = get_metrics(BM_classifier.classfier, X, y)
#knn_metrics = get_metrics(KNN_classifier, X, y)
#svm_metrics = get_metrics(SVM_classifier, X, y)
#rf_metrics = get_metrics(RF_classifier, X, y)
#nb_metrics = get_metrics(NB_classifier, X, y)

#result2 = zip(col , nb_metrics, rf_metrics, svm_metrics, knn_metrics, bm_metrics)

#write_predictions_to_csv(result1)
#write_metrics_to_csv(result2)

make_plots_for_classifier(vectorized_train_data,vectorized_test_data,categories)

