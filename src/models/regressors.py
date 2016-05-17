from __future__ import absolute_import

import traceback

import syringe

# Machine learning modules
from sklearn import ensemble
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn import tree

from sklearn.linear_model import SGDClassifier

from sklearn.metrics import r2_score


@syringe.provides('model-response')
class Response(object):
    """docstring for Response"""
    algorithm = None
    prediction = None
    accuracy_score = None
    label_test = None


@syringe.provides('linear-regressor')
class LinearReg(object):
    """docstring for ClassName"""
    def __init__(self):
        self.linear_reg = LinearRegression()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            print(train_y)
            self.linear_reg.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        print('I am predict')
        try:
            self.prediction = self.linear_reg.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        print('i give u accuracy')
        try:
            return r2_score(test_y, self.prediction)
        except:
            print(traceback.format_exc())


@syringe.provides('svm-linear-regressor')
class SvmLinearReg(object):
    """docstring for ClassName"""
    def __init__(self):
        self.svm_linear_reg = svm.SVR(kernel='linear', C=1e3)
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.svm_linear_reg.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.prediction = self.svm_linear_reg.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            return r2_score(test_y, self.prediction)
        except:
            print(traceback.format_exc())


@syringe.provides('decsion-tree-regressor')
class DecsionTreeReg(object):
    """docstring for ClassName"""
    def __init__(self):
        self.dt_linear_reg = tree.DecisionTreeRegressor()
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.dt_linear_reg.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.prediction = self.dt_linear_reg.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            return r2_score(test_y, self.prediction)
        except:
            print(traceback.format_exc())


@syringe.provides('randomforest-regressor')
class RandomForestReg(object):
    """docstring for ClassName"""
    def __init__(self):
        self.rf_linear_reg = ensemble.RandomForestRegressor(n_estimators=100)
        self.prediction = None
        self.train_x = None
        self.train_y = None

    def train_model(self, train_x, train_y):
        try:
            self.train_x = train_x
            self.train_y = train_y
            self.rf_linear_reg.fit(train_x, train_y)
        except:
            print(traceback.format_exc())

    def predict(self, test_x):
        try:
            self.prediction = self.rf_linear_reg.predict(test_x)
            return self.prediction
        except:
            print(traceback.format_exc())

    def accuracy_score(self, test_y):
        try:
            return r2_score(test_y, self.prediction)
        except:
            print(traceback.format_exc())

