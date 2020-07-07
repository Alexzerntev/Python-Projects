from sklearn.ensemble import VotingClassifier
from Helpers import svc_param_selection

from sklearn import preprocessing
from sklearn import svm

from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

class BeatTheBenchmark:

    def __init__(self, X, y):
        result = svc_param_selection(X, y, 2)
        self.SVM_classifier = svm.SVC(C=result['C'], kernel=result['kernel'],gamma=result['gamma'],decision_function_shape='ovo')
        self.RF_classifier = RandomForestClassifier(max_depth=50, n_estimators = 1200)
        self.KNN_classifier = KNeighborsClassifier(n_neighbors=8)
        self.classfier = VotingClassifier(estimators=[('SVM', self.SVM_classifier), ('RF', self.RF_classifier),  ('KNN', self.KNN_classifier)], voting='hard')

    def fit(self, X, y):
        return self.classfier.fit(X, y)
     
    def predict(self, T):
        return self.classfier.predict(T)
