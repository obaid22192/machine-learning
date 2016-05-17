# import tornado
import base64
import json
import traceback
import uuid
import datetime
from bson.objectid import ObjectId
from io import StringIO
import pandas as pd
import numpy as np
import syringe

import numpy as np
import pandas as pd
import pymongo

# custom modules

from src.mongodb import db_models

pd.set_option('chained_assignment', None)


@syringe.provides('mongodb-handler')
class MongoDbHandler(object):
    csv_data_handler = syringe.inject('csv-handler')
    """MongoDbHandler"""
    def __init__(self):
        self.db = None

    def project_ndb_to_domain(self, project):
        """
        The mongo repository for managing :class:`.Project` entities.

        """
        return db_models.Project(
            project_id=project['_id'],
            user_id=project['user_id'],
            project_name=project['project_name'],
            project_creation_date=project['project_creation_date']
        )

    def dataset_info_ndb_to_domain(self, data):
        """

        """
        return db_models.DatasetInfo(
            data_set_id=data['_id'],
            user_id=data['user_id'],
            project_id=data['project_id'],
            dataset_id=data['dataset_id'],
            dataset_name=data['dataset_name'],
            dataset_columns=data['dataset_columns']
        )

    def project_data_ndb_to_domain(self, data):
        """

        """
        return db_models.ProjectInfoData(
            project_data_id=data['_id'],
            project_id=data['project_id'],
            features=data['features'],
            labels=data['labels'],
            algorithms=data['algorithms'],
            test_size=data['test_size'],
            creation_timestamp=data['creation_timestamp']
        )

    def result_ndb_to_domain(self, result):
        """
        """
        return db_models.Results(
            accuracy_score=result['accuracy_score'],
            algorithm=result['algorithm'],
            label_test=result['label_test'],
            prediction=result['prediction'],
            experiment_id=result['experiment_id']
        )

    def store_data_set(self, **kwargs):
        """
        Creates new table in the database and store dataset that is uploaded
        by the user. Name for this dynamically created will be the combination
        of user_id + project-ID + file_name.
        After saveing dataset as a seperate collections this method stores the
        dataset's reference inside the dataset_info collection. User can retreive
        datasets information by project id and user id.

        """
        try:
            if not self.db:
                self.db = kwargs['db']
            file_name = kwargs['file_name']
            user = kwargs['user']
            project_id = kwargs['project_id']
            data_ = kwargs['data']
            user_id = self.get_user_from_current_db(user)['_id']
            # it would be greta to split data with regx.
            table_name = file_name.split('.')[0]
            # table_id = self.gen_uniq_id().decode("utf-8")
            table_id = str(user_id) + str(project_id) + table_name
            data_temp = StringIO(data_.replace('.', '_'))
            data = pd.read_csv(
                data_temp,
                sep=",",
                header=0,
                low_memory=False
            )
            del data_temp
            if self.db[table_id].insert(json.loads(data.to_json(
                orient='records'))
            ):
                d_info = self.db['dataset_info'].save(
                    db_models.DatasetInfo(
                        user_id=user_id,
                        project_id=[project_id],
                        dataset_id=table_id,
                        dataset_name=table_name,
                        dataset_columns=list(data.columns.values)
                    ))
                if d_info:
                    return self.dataset_info_ndb_to_domain(
                        db_models.DatasetInfo(
                            _id=d_info,
                            user_id=user_id,
                            project_id=[project_id],
                            dataset_id=table_id,
                            dataset_name=table_name,
                            dataset_columns=list(data.columns.values)
                        ))

        except Exception:
            raise

    def get_datasets_by_user_id(self, **kwargs):
        """
        Return all datasets belongs to particular user.

        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        try:
            print(user)
            user_id = self.get_user_from_current_db(user)['_id']
            datasets = self.db['dataset_info'].find({'user_id': user_id})
            return [(self.dataset_info_ndb_to_domain(data))
                    for data in datasets]
        except:
            print(traceback.format_exc())

    def delete_dataset_by_project_id(self, **kwargs):
        """
        Delete data matches the  project ID, This method will not delete the
        whole dataset from the database because that dataset might be used by
        another project.
        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        project_id = kwargs['project_id']
        dataset_id = kwargs['dataset_id']

        try:
            user_id = self.get_user_from_current_db(user)['_id']
            dataset_info = self.db['dataset_info'].find_one({
                '_id': ObjectId(dataset_id)
            })
            dataset_info['project_id'].remove(project_id)
            # delete dataset
            self.db['dataset_info'].update_many({
                'user_id': user_id,
                '_id': ObjectId(dataset_id)
            }, {
                '$set': {
                    'project_id': dataset_info['project_id']
                }
            })
            datasets = self.db['dataset_info'].find({'user_id': user_id})
            return [(self.dataset_info_ndb_to_domain(data))
                    for data in datasets]
        except:
            print(traceback.format_exc())
            return False

    def delete_dataset_by_data_id(self, **kwargs):
        """
        Delete data set by dataset id.
        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        dataset_id = kwargs['dataset_id']

        try:
            user_id = self.get_user_from_current_db(user)['_id']
            print('i ma daa')
            collection = self.db['dataset_info'].find_one({
                '_id': ObjectId(dataset_id),
                'user_id': user_id
            }, {
                'dataset_id': 1
            })
            print(collection)
            collection_name = collection['dataset_id']
            if collection_name in self.db.collection_names():
                self.db[collection_name].drop()
            self.db['dataset_info'].remove({
                '_id': ObjectId(dataset_id),
                'user_id': user_id
            })
            return True
        except pymongo.errors.PyMongoError as e:
            print(e)

    def add_dataset_to_project(self, **kwargs):
        """
        Add existing data set to given project.
        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        project_id = kwargs['project_id']
        dataset_id = kwargs['dataset_id']

        try:
            user_id = self.get_user_from_current_db(user)['_id']
            dataset_info = self.db['dataset_info'].find_one({
                '_id': ObjectId(dataset_id)
            })
            dataset_info['project_id'].append(project_id)
            # delete dataset
            self.db['dataset_info'].update_many({
                'user_id': user_id,
                '_id': ObjectId(dataset_id)
            }, {
                '$set': {
                    'project_id': dataset_info['project_id']
                }
            })
            datasets = self.db['dataset_info'].find({'user_id': user_id})
            return [(self.dataset_info_ndb_to_domain(data))
                    for data in datasets]
        except:
            print(traceback.format_exc())
            return False

    def gen_uniq_id(self, num_bytes=16):
        return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

    def create_user(self, **kwargs):
        """
        Creates a new user.

        """
        if not self.db:
            self.db = kwargs['db']
        email = kwargs['email']

        hashed_pass = kwargs['hashed_pass']

        try:
            self.db['users'].save(db_models.User(
                user_name='fake',
                email=email,
                password_hash=hashed_pass,
                user_creation_date=datetime.datetime.now()
            ))
            return True
        except:
            print(traceback.format_exc())
            return False

    def create_new_project(self, **kwargs):
        """
        Creates a new project.

        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        # get user from database
        user_id = self.get_user_from_current_db(user)['_id']
        project_name = kwargs['project_name']
        try:
            new_project = db_models.Project(
                user_id=user_id,
                project_name=project_name,
                project_creation_date=datetime.datetime.now()
            )
            _id = self.db['projects'].save(new_project)
            if _id:
                new_project._id = _id
                return self.project_ndb_to_domain(new_project)
        except:
            print(traceback.format_exc())
            return False

    def get_projects(self, **kwargs):
        """
        Return all projects belongs to particular user.

        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        # get user from database

        try:
            user_id = self.get_user_from_current_db(user)['_id']
            # get projects from database
            projects = self.db['projects'].find({'user_id': user_id})
            return [(self.project_ndb_to_domain(project))
                    for project in projects]
        except:
            print(traceback.format_exc())

    def delete_project_by_id(self, **kwargs):
        """
        Delete project with particular ID
        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        project_id = kwargs['project_id']

        try:
            user_id = self.get_user_from_current_db(user)['_id']
            # delete project
            self.db['projects'].remove({'user_id': user_id} and
                                       {'_id': ObjectId(project_id)})
        except:
            print(traceback.format_exc())

    def get_projects_by_id(self, **kwargs):
        """
        Return project for given id and belongs to current user.

        """
        if not self.db:
            self.db = kwargs['db']
        user = kwargs['user']
        project_id = kwargs['project_id']
        # get user from database

        try:
            user_id = self.get_user_from_current_db(user)['_id']
            # get projects from database
            projects = self.db['projects'].find({'user_id': user_id} and
                                                {'_id': ObjectId(project_id)})
            return [(self.project_ndb_to_domain(project))
                    for project in projects]
        except:
            print(traceback.format_exc())

    def get_user_from_current_db(self, email):
        """
        Get user from database using email(current_user).
        """
        return self.db['users'].find_one({'email': email})

    def load_project(self, **kwargs):
        """
        This method load current project to process by the machine learning
        alogorithms.

        Args:
            user_id (str): current user's id.

            project_id (str): Id of the current project that need to be
                            processed.
            collection (str): Name of the dataset that need to be loaded.
        """

        if not self.db:
            self.db = kwargs['db']
        data = kwargs['data']
        user = kwargs['user']
        project_id = data['project_id']
        # collection = kwargs['collection']
        features_raw = json.loads(data['features'])
        labels_raw = json.loads(data['labels'])
        uniq_dataset_feat = list(
            set([value['dataset']
                for value in features_raw])
        )
        uniq_dataset_labels = list(
            set([value['dataset']
                for value in labels_raw])
        )

        features = [{'dataset_id': d, 'columns': []}
                    for d in uniq_dataset_feat]
        labels = [{'dataset_id': d, 'columns': []}
                  for d in uniq_dataset_labels]

        [f['columns'].append(value['feature']) for value in features_raw
            for f in features
            if f['dataset_id'] in value['dataset']]

        [l['columns'].append(value['lable']) for value in labels_raw
            for l in labels
            if l['dataset_id'] in value['dataset']]
        x = []
        y = []
        for f in features:
            col_id = self.db['dataset_info'].find_one(
                {
                    '_id': ObjectId(f['dataset_id'])
                }, {
                    'dataset_id': 1
                })
            print(col_id['dataset_id'])

            # x.append(self.db[col_id['dataset_id']])
            x.append(list(self.db[col_id['dataset_id']].find({}, {
                c: 1 for c in f['columns']
            })))

        for l in labels:
            col_id = self.db['dataset_info'].find_one(
                {
                    '_id': ObjectId(l['dataset_id'])
                }, {
                    'dataset_id': 1
                })
            print(col_id['dataset_id'])
            y.append(list(self.db[col_id['dataset_id']].find({}, {
                c: 1 for c in l['columns']
            })))
        self.csv_data_handler.add_features(x)
        self.csv_data_handler.add_to_predict(y)
        self.csv_data_handler.run(test_size=data['test_size'])
        return True

    def save_project_data(self, **kwargs):
        """
        This method load current project to process by the machine learning
        alogorithms.

        Args:
            user_id (str): current user's id.

            project_id (str): Id of the current project that need to be
                            processed.
            collection (str): Name of the dataset that need to be loaded.
        """

        if not self.db:
            self.db = kwargs['db']
        # user = kwargs['user']
        data = kwargs['data']
        project_id = data['project_id']
        algorithms = data['algorithms']
        # collection = kwargs['collection']
        pd_data = db_models.ProjectInfoData(
            project_id=project_id,
            features=data['features'],
            labels=data['labels'],
            creation_timestamp=datetime.datetime.now(),
            algorithms=algorithms,
            test_size=data['test_size']
        )
        pd = self.db['project_data'].save(pd_data)
        if pd:
            return self.project_data_ndb_to_domain(pd_data)

    def retrieve_experiments_by_project_id(self, **kwargs):
        """
        This method returns all experiments belongs to particular
        project.

        Args:
            user_id (str): current user's id.

            project_id (str): Id of the current project that need to be
                            processed.
        """

        if not self.db:
            self.db = kwargs['db']
        project_id = kwargs['project_id']
        experiments = self.db['project_data'].find(
            {
                'project_id': project_id
            }
        )
        for ex in experiments:
            yield self.project_data_ndb_to_domain(ex)

    def save_experiment_results(self, **kwargs):
        """
        This method saves the ruselts for an experiment.
        """
        try:
            if not self.db:
                self.db = kwargs['db']
            # user = kwargs['user']
            results = kwargs['results']
            # collection = kwargs['collection']
            for result in results:
                self.db['results'].save(db_models.Results(
                    accuracy_score=result['accuracy_score'],
                    algorithm=result['algorithm'],
                    label_test=result['label_test'],
                    prediction=result['prediction'],
                    experiment_id=kwargs['experiment_id']
                ))
            return True
        except:
            print(traceback.format_exc())
            return False

    def retrieve_results_experiment_id(self, **kwargs):
        """
        Return experiment results by experiment id.

        """
        if not self.db:
            self.db = kwargs['db']
        ex_id = kwargs['experiment_id']
        # get user from database
        try:
            results = self.db['results'].find({'experiment_id': ex_id})
            return [(self.result_ndb_to_domain(res))
                    for res in results]
        except:
            print(traceback.format_exc())
            return False
