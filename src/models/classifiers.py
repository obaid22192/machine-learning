from __future__ import absolute_import

import traceback

import syringe

from sklearn.linear_model import SGDClassifier

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from sklearn.metrics import r2_score


@syringe.provides('sgd-classifier')
class SGDCls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.sgd_cls = SGDClassifier()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            print(self.train_y)
            self.sgd_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.prediction = self.sgd_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            return r2_score(test_y, self.prediction)
        except:
            print(traceback.format_exc())


@syringe.provides('kneighbors-classifier')
class KNeighborsCls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.kneighbors_cls = KNeighborsClassifier(3)
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.kneighbors_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.prediction = self.kneighbors_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            return r2_score(test_y, self.prediction)
        except:
            print(traceback.format_exc())


@syringe.provides('svm-classifier')
class SVMcls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.svm_cls = SVC(gamma=2, C=1)
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.svm_cls.fit(train_x, train_y)
            print('i am traing this model')
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.svm_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.svm_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())


@syringe.provides('decisiontree-classifier')
class DecisionTreecls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.decision_tree_cls = DecisionTreeClassifier(max_depth=5)
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.decision_tree_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.decision_tree_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.decision_tree_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())


@syringe.provides('randomforest-classifier')
class RandomForestcls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.rf_cls = RandomForestClassifier(
            max_depth=5,
            n_estimators=10,
            max_features=1
        )
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.rf_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.rf_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.rf_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())


@syringe.provides('adaboost-classifier')
class AdaBoostcls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.adaboost_cls = AdaBoostClassifier()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.adaboost_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.adaboost_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.adaboost_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())


@syringe.provides('gaussiannb-classifier')
class GaussianNBcls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.gnb_cls = GaussianNB()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.gnb_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.gnb_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.gnb_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())


@syringe.provides('lineardiscriminantanalysis-classifier')
class LinearDiscriminantAnalysiscls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.lda_cls = LinearDiscriminantAnalysis()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.lda_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.lda_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.lda_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())


@syringe.provides('quadraticdiscriminantanalysis-classifier')
class QuadraticDiscriminantAnalysiscls(object):
    """docstring for ClassName"""
    def __init__(self):
        self.qda_cls = QuadraticDiscriminantAnalysis()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.qda_cls.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.test_x = test_x
            self.prediction = self.qda_cls.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            # return r2_score(test_y, self.prediction)
            return self.qda_cls.score(self.test_x, test_y)
        except:
            print(traceback.format_exc())
