import pandas as pd

from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import cross_val_score

from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from Helpers import *

def make_plots_for_classifier(vectorized_train_data,vectorized_test_data,categories):
    # performing LSI
    SVM_components = []
    SVM_accuracy = []
    RF_components = []
    RF_accuracy = []
    NB_components = []
    NB_accuracy = []
    KNN_components = []
    KNN_accuracy = []
    for comp in range(10,260,20):
        X = TruncatedSVD(n_components = comp).fit_transform(vectorized_train_data)
        T = TruncatedSVD(n_components = comp).fit_transform(vectorized_test_data)

        # Building encoder and transforming categories
        labelEncoder = preprocessing.LabelEncoder()
        y = labelEncoder.fit(categories).transform(categories)

        # Support Vector Machines 
        result = svc_param_selection(X, y, 10)
        SVM_classifier = svm.SVC(C=result['C'], kernel=result['kernel'],gamma=result['gamma'],decision_function_shape='ovo')
        SVM_classifier.fit(X, y)
    
        ## Support Vector Machines 
        ##SVM_classifier = svm.SVC(decision_function_shape='ovo')
        ##SVM_classifier.fit(X, y)

        ## Random forests
        RF_classifier = RandomForestClassifier()
        RF_classifier.fit(X, y)

        ## Naive Bayes
        NB_classifier = GaussianNB()
        NB_classifier.fit(X, y)

        SVM_components.append(comp)
        SVM_accuracy.append(accuracy_comp(SVM_classifier, X, y))

        RF_components.append(comp)
        RF_accuracy.append(accuracy_comp(RF_classifier, X, y))

        NB_components.append(comp)
        NB_accuracy.append(accuracy_comp(NB_classifier, X, y))
    
    make_plot(SVM_components,SVM_accuracy,250,1,'-SVM-','Accuracy','Components')
    make_plot(RF_components,RF_accuracy,250,1,'-RF-','Accuracy','Components')
    make_plot(NB_components,NB_accuracy,250,1,'-NB-','Accuracy','Components')
