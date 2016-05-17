# encoding: utf-8

from __future__ import absolute_import

import syringe
import bcrypt
import functools
import logging
from bson import ObjectId
import datetime
import json
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado import gen

from src import Algorithms


def custom_encoder(self, obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return str(obj)

json.JSONEncoder.default = custom_encoder


def authenticated_async(f):
    @functools.wraps(f)
    @tornado.web.asynchronous
    def wrapper(self, *args, **kwargs):
        self.current_user = self.get_current_user()
        if self.current_user:
            logging.info('User successfully authenticated')
            f(self, *args, **kwargs)
        else:
            raise tornado.web.HTTPError(401, 'User not authenticated, '
                                             'aborting')
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin",
                        self.request.headers['Origin'])
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "accept")

    def get_login_url(self):
        return u"/login"

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            kwargs['message'] = 'Unknown Error: '
        self.write(kwargs['message'])

    @authenticated_async
    def get(self):
        # print(self.settings['cookie_secret'])
        if not self.current_user:
            print('you are differnt user')
        else:
            print('current' + self.current_user)

        self.render("upload.html")

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None


class PredictHandler(BaseHandler):
    reg_service = syringe.inject('regressor-service')
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        self.write(json.dumps([p for p in Algorithms]))
        self.finish()

    @authenticated_async
    def post(self):
        self.set_header('Content-Type', 'application/json')
        data = tornado.escape.json_decode(self.request.body)
        response = self.reg_service.train_model(
            data=data,
            user=self.current_user,
            db=self.application.syncdb
        )
        self.mongodb_service.save_experiment_results(
            results=response,
            db=self.application.syncdb,
            experiment_id=data['project_data_id']
        )
        self.set_header('Content-Type', 'application/json')
        self.set_header(
            'Cache-Control',
            'no-store, no-cache, must-revalidate, max-age=0'
        )
        self.write(tornado.escape.json_encode([r for r in response]))
        self.finish()


class RetrieveResultsHandler(BaseHandler):
    """
    Handler to return results those belongs to given experment.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self, experiment_id):
        self.set_header('Content-Type', 'application/json')
        results = self.mongodb_service.retrieve_results_experiment_id(
            experiment_id=experiment_id,
            db=self.application.syncdb
        )
        self.write(json.dumps([r for r in results]))
        self.finish()


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    # @gen.coroutine
    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "").encode('utf-8')
        user = self.application.syncdb['users'].find_one({'email': email})
        # Warning bcrypt will block IO loop:
        if user and user['password_hash'] and bcrypt.hashpw(password, user['password_hash']) == user['password_hash']:
            self.set_current_user(email)
        else:
            self.set_secure_cookie('flash', "Login incorrect")
            raise tornado.web.HTTPError(400, 'Loign Failed, '
                                             'aborting')

    def set_current_user(self, user):
        print('setting ' + user)
        if user:
            self.write('you are logged In Now ')
            self.set_secure_cookie("user", tornado.escape.json_encode(user), 10)
        else:
            self.clear_cookie("user")
            self.write('you are Not Logged In')


class RegisterHandler(LoginHandler):
    mongodb_service = syringe.inject('mongodb-service')

    def get(self):
        self.render('register.html')

    def post(self):
        email = self.get_argument("email", "")

        already_taken = self.application.syncdb['users'].find_one({'email': email})
        if already_taken:
            return

        # Warning bcrypt will block IO loop:
        password = self.get_argument("password", "").encode('utf-8')

        hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt(8))

        user = {}
        user['user'] = email
        user['password'] = hashed_pass
        if self.mongodb_service.create_user(
            email=email,
            hashed_pass=hashed_pass,
            db=self.application.syncdb
        ):
            self.set_current_user(email)
        else:
            raise tornado.web.HTTPError(400, 'Registration Failed, '
                                             'aborting')
        self.finish()


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write('You are logged-Out Now')
        self.redirect('/')
        self.finish()


class CreateProjectHandler(BaseHandler):
    mongodb_service = syringe.inject('mongodb-service')

    # @gen.coroutine
    @authenticated_async
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        self.set_header(
            'Cache-Control',
            'no-store, no-cache, must-revalidate, max-age=0'
        )
        self.set_header('Content-Type', 'application/json')
        project_name = self.get_argument("project_name", "")
        project = self.mongodb_service.create_new_project(
            user=self.current_user,
            project_name=project_name,
            db=self.application.syncdb
        )
        self.write(json.dumps(project))
        self.finish()


class ProjectsHandler(BaseHandler):
    """
    Handler to return projects those belongs to current user.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        projects = self.mongodb_service.get_projects(
            user=self.current_user,
            db=self.application.syncdb
        )
        self.write(json.dumps([p for p in projects]))
        self.finish()


class ProjectHandler(ProjectsHandler):
    """
    Handler to return project that matches the project id.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self, p_id):
        self.set_header('Content-Type', 'application/json')
        projects = self.mongodb_service.get_projects_by_id(
            user=self.current_user,
            project_id=p_id,
            db=self.application.syncdb
        )
        self.write(json.dumps([p for p in projects]))
        self.finish()

    @authenticated_async
    @tornado.web.asynchronous
    def delete(self, p_id):
        print('Deleteing in progress..')
        self.set_header('Content-Type', 'application/json')
        self.mongodb_service.delete_project(
            user=self.current_user,
            project_id=p_id,
            db=self.application.syncdb
        )
        self.finish('DELETING DONE!')


class UploadDataHandler(BaseHandler):
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        datasets = self.mongodb_service.get_datasets_by_user_id(
            user=self.current_user,
            db=self.application.syncdb
        )
        self.write(json.dumps([d for d in datasets]))
        self.finish()

    @authenticated_async
    @tornado.web.asynchronous
    def post(self, project_id):
        try:
            file1 = self.request.files['file'][0]
            response = self.mongodb_service.store_data_set(
                user=self.current_user,
                project_id=project_id,
                db=self.application.syncdb,
                file_name=file1['filename'],
                data=file1['body'].decode("utf-8")
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(response))
            self.finish()
        except:
            self.send_error(
                400,
                message='File upload failed! kindly check your file for errors and try again.'
            )


class DeleteDataByProjectDataHandler(BaseHandler):
    """
    This method is used to delete data set belongd to given project,
    we are useing the get request to trigger delete, this is very bad
    approach, we need to use delete method to acomplish this task.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self, p_id, d_id):
        # self.set_header('Content-Type', 'application/json')
        datasets = self.mongodb_service.delete_dataset_by_project_id(
            user=self.current_user,
            project_id=p_id,
            dataset_id=d_id,
            db=self.application.syncdb
        )
        if datasets:
            self.write(json.dumps([d for d in datasets]))
        else:
            raise tornado.web.HTTPError(404, 'No dataset found, aborting')
        self.finish()


class AddDataToProjectDataHandler(BaseHandler):
    """
    This method is used to delete data set belongd to given project,
    we are useing the get request to trigger delete, this is very bad
    approach, we need to use delete method to acomplish this task.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def post(self, p_id, d_id):
        # self.set_header('Content-Type', 'application/json')
        datasets = self.mongodb_service.add_dataset_to_project(
            user=self.current_user,
            project_id=p_id,
            dataset_id=d_id,
            db=self.application.syncdb
        )
        if datasets:
            self.write(json.dumps([d for d in datasets]))
        else:
            raise tornado.web.HTTPError(404, 'No dataset found, aborting')
        self.finish()


class DeleteDataHandler(BaseHandler):
    """
    This method is used to delete data set
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self, dataset_id):
        # self.set_header('Content-Type', 'application/json')
        self.mongodb_service.delete_dataset_by_data_id(
            user=self.current_user,
            dataset_id=dataset_id,
            db=self.application.syncdb
        )
        self.finish()


class RetrieveDataSetHandler(BaseHandler):
    """
    Retrieve all datasets belongs to current user.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        datasets = self.mongodb_service.get_datasets_by_user_id(
            user=self.current_user,
            db=self.application.syncdb
        )
        self.write(json.dumps([d for d in datasets]))
        self.finish()


class SaveCurrentExperimentHandler(BaseHandler):
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    def post(self):
        self.set_header('Content-Type', 'application/json')

        data = tornado.escape.json_decode(self.request.body)
        response = self.mongodb_service.save_project_data(
            user=self.current_user,
            db=self.application.syncdb,
            data=data
        )
        self.write(json.dumps(response))
        self.finish()


class RetrieveExperimentsHandler(BaseHandler):
    """
    Retrieve all experiments belongs to given project.
    """
    mongodb_service = syringe.inject('mongodb-service')

    @authenticated_async
    @tornado.web.asynchronous
    def get(self, project_id):
        self.set_header('Content-Type', 'application/json')
        response = self.mongodb_service.retrieve_experiments_by_project_id(
            project_id=project_id,
            db=self.application.syncdb
        )
        self.write(json.dumps([ex for ex in response]))
        self.finish()
