# Import required pyhton modules.

import traceback
# Data processing modules
import numpy as np
import pandas as pd

import syringe

from sklearn.cross_validation import train_test_split
from sklearn import preprocessing


pd.set_option('chained_assignment', None)


class KeyboardInterruptError(Exception):
    pass


@syringe.provides('csv-handler')
class CsvLoader(object):
    """docstring for CsvLoader"""

    def __init__(self):
        self.project_id = None
        self.user_id = None
        self.data_frame = None
        self.features = None
        self.to_predict = None
        self.x = None
        self.y = None
        self.train_x = None
        self.test_x = None
        self.train_y = None
        self.test_y = None
        self.test_size = 0.1
        self.file_name = None
        self.sentiment_article = None

    def load_data(self, collection):
        """
        Populate the dataframe.

        Args:
            collection (DatasetInfo): Dataset inside database that need to be
            loaded in to dataframe.
        """
        try:
            # print(list(collection.find()))
            # self.data_frame = pd.DataFrame(
            #     list(collection.find({}, {"Month": 1}))
            # )
            self.data_frame = pd.DataFrame(
                list(collection.find())
            )
            del self.data_frame['_id']
            print(self.data_frame)
        except:
            print(traceback.format_exc())
        else:
            return True

    def normalize_date_to_eustandards(self):
        """
        Normalize dataes to european style!
        """
        try:
            self.data_frame['ORD_REQUESTDELIVERYDATE'] = pd.to_datetime(
                pd.Series(self.data_frame['ORD_REQUESTDELIVERYDATE'])
            )
            self.data_frame['ORD_ORDERDATE'] = pd.to_datetime(pd.Series(
                self.data_frame['ORD_ORDERDATE'])
            )
            self.data_frame['ORD_CREATIONDATE'] = pd.to_datetime(
                pd.Series(self.data_frame['ORD_CREATIONDATE'])
            )
        except:
            print(traceback.format_exc())

    def get_columns(self):
        """
        Get column's header of the dataframe
        """

        return self.data_frame.columns.values.tolist()

    def add_features(self, x):
        """
        Add features to to the x-axis currently we are cleaning
        and adding features manually but later this process should
        be handel in front end.
        """
        try:
            self.features = pd.DataFrame()
            for da in x:
                self.features = pd.concat(
                    [self.features, pd.DataFrame(da)],
                    axis=1
                )
            del self.features['_id']
            # if(self.features.isnull().values.any()):
            self.features = self.features.fillna(0)
            self.features = self.features.replace('None', 0)
            # self.features = self.features.replace('_', '.')
            self.features = self.features.applymap(
                lambda x: x.replace('_', '.') if isinstance(x, str) else x
            )

            self.features = self.features[0:].astype(str)
            self.features = self.features.apply(preprocessing.LabelEncoder().fit_transform)
            return True
        except:
            print(traceback.format_exc())
            raise
        else:
            return False

    def drop_features(self, x=None):
        try:
            self.features.drop(x, inplace=True, axis=1)
        except:
            print(traceback.format_exc())
        else:
            return False

    def add_to_predict(self, y):
        try:
            self.to_predict = pd.DataFrame(index=self.features.index)
            for da in y:
                self.to_predict = pd.concat(
                    [self.to_predict, pd.DataFrame(da)],
                    axis=1
                )
            del self.to_predict['_id']
            self.to_predict = self.to_predict.fillna(0)
            self.to_predict = self.to_predict.replace('None', 0)

            self.to_predict = self.to_predict.applymap(
                lambda x: x.replace('_', '.').strip() if isinstance(x, str) else x
            )
            self.to_predict = self.to_predict[0:].astype(float)
            print(self.to_predict)
        except:
            print(traceback.format_exc())
        else:
            return False

    def drop_to_predict(self, x=None):
        try:
            self.to_predict.drop(x, inplace=True, axis=1)
        except:
            print(traceback.format_exc())
        else:
            return False

    def set_index(self, index_):
        """docstring for set_index"""

        try:
            self.data_frame.index = self.data_frame[index_]
        except:
            print(traceback.format_exc())

    def clear_dataframe(self):
        try:
            self.data_frame = None
        except:
            print(traceback.format_exc())

    def clear_features(self):
        try:
            self.features = None
        except:
            print(traceback.format_exc())

    def set_axis(self):
        try:
            self.x = self.features.as_matrix(
                columns=self.features.columns
            )
            self.y = self.to_predict[0:].values.ravel()
            self.y = self.y.astype(int)
        except:
            print(traceback.format_exc())

    def split_data(self, x, y, random_state=0):
        """
        Split data in to train and test data set, this method is wrapper around
         the cross_validation's train_test_split method.

        Args:
            X :  x-axis
            Y
            test_size (float): Size of the test data default size is 25
            percent.

            random_state (int): Defines the behaviour of data split.

        Return:
            X_train, X_test, Y_train, Y_test: Splited data that will be feeded
             in to the model
        """
        try:
            return train_test_split(
                x, y, test_size=self.test_size, random_state=random_state
            )
        except:
            print(traceback.format_exc())

    # def start_multi(self):

    def run(self, **kwargs):
        try:
            self.set_axis()
            self.test_size = (int(kwargs['test_size']) / 100)
            if self.test_size <= 0.0 or self.test_size >= 1:
                self.test_size = 0.1
            self.train_x, self.test_x, self.train_y, self.test_y = self.split_data(self.x, self.y)
        except Exception:
            print(traceback.format_exc())
        except KeyboardInterrupt:
            raise KeyboardInterruptError()
