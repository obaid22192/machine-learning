import syringe
# Dependices
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np


@syringe.provides('textsentiment-obj')
class TextSentiment(object):
    def __int__(self):
        self.train = None
        self.text_clf = None
        self.predicted = None

    def train(self):
        """Loading and Training classifier"""
        # Load dataset
        categories = ['neg', 'pos']
        self.train_set = load_files('resources/sentimentDataset/train/', categories=categories, encoding='latin-1')
        self.test_set = load_files('resources/sentimentDataset/test/', categories=categories, encoding='latin-1')

        #Tokenizing text with scikit-learn
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(self.train_set.data)

        # occurrences to frequencies
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        # Pipline
        self.text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])
        self.text_clf.fit(self.train_set.data, self.train_set.target)

    def predict(self, article):
        self.predicted = self.text_clf.predict([article])
        if 1 in self.predicted:
            return 'Article is Postive'
        else:
            return 'Article is Negative'

            docs_test = self.test_set.data
            self.predicted = self.text_clf.predict(docs_test)
            print(str(np.mean(self.predicted == self.test_set.target)*100), 'Accuracy')
            return self.predicted

    def getStats(self):
        print(metrics.classification_report(self.test_set.target, self.predicted,target_names=self.test_set.target_names))
