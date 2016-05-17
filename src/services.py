from __future__ import absolute_import

import traceback
from multiprocessing import Pool

import syringe


class KeyboardInterruptError(Exception):
    pass


@syringe.provides('regressor-service')
class RegService(object):
    """
    The service layer for :class:`.LinearReg`.
    """

    csv_data_handler = syringe.inject('csv-handler')

    linear_reg = syringe.inject('linear-regressor')
    svm_linear_reg = syringe.inject('svm-linear-regressor')
    random_forest_reg = syringe.inject('randomforest-regressor')
    decsion_tree_reg = syringe.inject('decsion-tree-regressor')
    model_response = syringe.inject('model-response')

    sgd_classifier = syringe.inject('sgd-classifier')
    kneighbors_classifier = syringe.inject('kneighbors-classifier')
    svm_classifier = syringe.inject('svm-classifier')
    decsion_tree_classifier = syringe.inject('decisiontree-classifier')
    random_forest_classifier = syringe.inject('randomforest-classifier')

    ada_boost_classifier = syringe.inject('adaboost-classifier')
    gaussiannb_classifier = syringe.inject('gaussiannb-classifier')
    linear_discriminantan_alysis_classifier = syringe.inject('lineardiscriminantanalysis-classifier')
    quadratic_discriminant_analysiscls_classifier = syringe.inject('quadraticdiscriminantanalysis-classifier')
    mongodb_handler = syringe.inject('mongodb-handler')

    naive_bayes = syringe.inject('textsentiment-obj')

    def parallel(self, reg_):
        # print(self.csv_data_handler.train_x)
        m = str(reg_).strip()
        if 'naive_bayes' in m:
            self.model_response.accuracy_score = 0.85
            self.model_response.algorithm = str(reg_).strip()
            self.model_response.prediction = [self.naive_bayes.predict(self.csv_data_handler.sentiment_article)]
            self.model_response.label_test = [self.csv_data_handler.sentiment_article]
            return self.model_response.__dict__
        else:
            model_ = self.algorithms.get(m)
            model_.train_model(self.csv_data_handler.train_x,
                               self.csv_data_handler.train_y)
            self.model_response.prediction = model_.predict(
                self.csv_data_handler.test_x
            ).tolist()

            self.model_response.accuracy_score = model_.accuracy_score(
                self.csv_data_handler.test_y
            )
            self.model_response.algorithm = str(reg_).strip()
            self.model_response.label_test = self.csv_data_handler.test_y.tolist()
            # return {'accuracy_score': self.model_response.accuracy_score}
            return self.model_response.__dict__

    def train_model(self, **kwargs):
        data = kwargs['data']
        self.algorithms = {
            'linear_reg': self.linear_reg,
            'svm_linear_reg': self.svm_linear_reg,
            'random_forest_reg': self.random_forest_reg,
            'decsion_tree_reg': self.decsion_tree_reg,
            'sgd_classifier': self.sgd_classifier,
            'kneighbors_classifier': self.kneighbors_classifier,
            'svm_classifier': self.svm_classifier,
            'decsion_tree_classifier': self.decsion_tree_classifier,
            'random_forest_classifier': self.random_forest_classifier,
            'ada_boost_classifier': self.ada_boost_classifier,
            'gaussiannb_classifier': self.gaussiannb_classifier,
            'linear_discriminantan_alysis_classifier': self.linear_discriminantan_alysis_classifier,
            'quadratic_discriminant_analysiscls_classifier': self.quadratic_discriminant_analysiscls_classifier,
            'naive_bayes': self.naive_bayes
        }

        params = []
        for algo in data['algorithms']:
            if 'LinearRegression' in algo:
                params.append('linear_reg')
            elif 'Svm Linear Regression' in algo:
                params.append('svm_linear_reg')
            elif 'Decision Tree Regression' in algo:
                params.append('decsion_tree_reg')
            elif 'Random Forest Regression' in algo:
                params.append('random_forest_reg')
            elif 'SGD Classifier' in algo:
                params.append('sgd_classifier')
            elif 'KNeighborsClassifier' in algo:
                params.append('kneighbors_classifier')
            elif 'Svm Classifier' in algo:
                params.append('svm_classifier')
            elif 'Decision Tree Classifier' in algo:
                params.append('decsion_tree_classifier')
            elif 'Random Forest Classifier' in algo:
                params.append('random_forest_classifier')
            elif 'Ada Boost Classifier' in algo:
                params.append('ada_boost_classifier')
            elif 'Gaussian Nb Classifier' in algo:
                params.append('gaussiannb_classifier')
            elif 'Linear Discriminant Analysis Classifier' in algo:
                params.append('linear_discriminantan_alysis_classifier')
            elif 'Quadratic Discriminant Analysiscls Classifier' in algo:
                params.append('quadratic_discriminant_analysiscls_classifier')
            elif 'Sentiment-Analysis' in algo:
                if data['article']:
                    self.csv_data_handler.sentiment_article = data['article']
                params.append('naive_bayes')

        self.mongodb_handler.load_project(**kwargs)
        pool = Pool(len(params))
        try:
            response = pool.map_async(self.parallel, params)
            pool.close()
            pool.join()
            return response.get()

        except Exception:
            pool.terminate()
            print(traceback.format_exc())
        except KeyboardInterrupt:
            pool.join()
            raise KeyboardInterruptError()
        finally:
            pool.terminate()


@syringe.provides('classification-service')
class ContextAwarenesservices(object):
    """
    service layer for classification-service
    """
    text_blob = syringe.inject('textblob-response')

    def textblob_run(self, sentence):
        self.text_blob.run(sentence)


@syringe.provides('mongodb-service')
class MongoDbService(object):
    """
    The service layer for :class:`MongoDbHandler.`
    """
    mongodb_handler = syringe.inject('mongodb-handler')

    def store_data_set(self, **kwargs):
        try:
            return self.mongodb_handler.store_data_set(**kwargs)
        except:
            raise

    def get_datasets_by_user_id(self, **kwargs):
        return self.mongodb_handler.get_datasets_by_user_id(**kwargs)

    def delete_dataset_by_project_id(self, **kwargs):
        return self.mongodb_handler.delete_dataset_by_project_id(**kwargs)

    def load_project(self, **kwargs):
        return self.mongodb_handler.load_project(**kwargs)

    def create_user(self, **kwargs):
        return self.mongodb_handler.create_user(**kwargs)

    def create_new_project(self, **kwargs):
        return self.mongodb_handler.create_new_project(**kwargs)

    def get_projects(self, **kwargs):
        return self.mongodb_handler.get_projects(**kwargs)

    def get_projects_by_id(self, **kwargs):
        return self.mongodb_handler.get_projects_by_id(**kwargs)

    def delete_project(self, **kwargs):
        return self.mongodb_handler.delete_project_by_id(**kwargs)

    def save_project_data(self, **kwargs):
        return self.mongodb_handler.save_project_data(**kwargs)

    def retrieve_experiments_by_project_id(self, **kwargs):
        return self.mongodb_handler.retrieve_experiments_by_project_id(**kwargs)

    def delete_dataset_by_data_id(self, **kwargs):
        return self.mongodb_handler.delete_dataset_by_data_id(**kwargs)

    def add_dataset_to_project(self, **kwargs):
        return self.mongodb_handler.add_dataset_to_project(**kwargs)

    def save_experiment_results(self, **kwargs):
        return self.mongodb_handler.save_experiment_results(**kwargs)

    def retrieve_results_experiment_id(self, **kwargs):
        return self.mongodb_handler.retrieve_results_experiment_id(**kwargs)
