import pandas as pd

import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

def make_plot(list1,list2,x_max,y_max,classifier,y,x):
    plt.axis([10, x_max, 0, y_max])
    plt.plot(list1,list2)
    plt.title(classifier)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.show()

def accuracy_comp(classifier, X, y):

    accuracy = cross_val_score(classifier, X, y, cv=10, scoring = 'accuracy')
    return accuracy.mean()

def svc_param_selection(X, y, nfolds):
    Cs = [0.001, 0.01, 0.1, 1, 10]
    gammas = [0.001, 0.01, 0.1, 1]
    kernel = ['rbf']
    param_grid = {'C': Cs, 'gamma' : gammas, 'kernel' : kernel}
    grid_search = GridSearchCV(svm.SVC(kernel), param_grid=param_grid, cv=nfolds)
    grid_search.fit(X, y)
    grid_search.best_params_
    return grid_search.best_params_

def write_predictions_to_csv(predictions):
    result = {
            "ID":[],
            "Predicted_Category":[]
        }
    for x,y in predictions:
        result["ID"].append(x)
        result["Predicted_Category"].append(y)
    data_frame = pd.DataFrame(result, columns= ['ID', "Predicted_Category"])
    data_frame.to_csv("testSet_categories.csv", sep="\t", index = False, index_label = False)

def write_metrics_to_csv(metrics):
    result = {
            "Statistic Measure":[],
            "Naive Bayes":[],
            "Random Forest":[],
            "SVM":[],
            "KNN":[],
            "My Method":[]
        }
    for x,y,z,k,n,l in metrics:
        result["Statistic Measure"].append(x)
        result["Naive Bayes"].append(y)
        result["Random Forest"].append(z)
        result["SVM"].append(k)
        result["KNN"].append(n)
        result["My Method"].append(l)
    data_frame = pd.DataFrame(result, columns= ['Statistic Measure', "Naive Bayes", "Random Forest", "SVM", "KNN", "My Method"])
    data_frame.to_csv("EvaluationMetric_10fold.csv", sep="\t", index = False, index_label = False)