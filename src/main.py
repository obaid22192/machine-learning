from __future__ import absolute_import

import socket
import base64
import uuid
# import M2Crypto
import tornado
from tornado import httpserver, netutil
import tornado.wsgi
import wsgiref.simple_server
from tornado.web import url
from tornado.options import define
from tornado.options import options
from pymongo import MongoClient

from src.data_handlers.csv_handler import CsvLoader
from src.data_handlers.mongodb_handler import MongoDbHandler
from src.models import regressors
from src.models import classifiers
from src import services
from src.models.regressors import Response
from src.models.textsentiment import TextSentiment
from src import api


define('port', default=8901, type=int)

try:
    _ip = socket.gethostbyname(socket.gethostname())

    if _ip.startswith("127."):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))  # address doesn't send packets
        _ip = s.getsockname()[0]

except:
    print('Network is down falling back to the local host.')
    _ip = 'localhost'

define('address', _ip)


# MONGO_SERVER = '192.168.1.68'
MONGO_SERVER = 'localhost'


def init_csvloader():
    """
    Initialise csv data module.

    """
    CsvLoader()
    MongoDbHandler()


def init_regressors():
    """
    Initialise the ml modules.

    """
    regressors.LinearReg()
    regressors.SvmLinearReg()
    regressors.DecsionTreeReg()
    regressors.RandomForestReg()


def init_classifiers():
    classifiers.SGDCls()
    classifiers.KNeighborsCls()
    classifiers.SVMcls()
    classifiers.DecisionTreecls()
    classifiers.RandomForestcls()
    classifiers.AdaBoostcls()
    classifiers.GaussianNBcls()
    classifiers.LinearDiscriminantAnalysiscls()
    classifiers.QuadraticDiscriminantAnalysiscls()


def init_services():
    """
    Initialise the services used by the core framework.

    """
    services.RegService()
    services.ContextAwarenesservices()
    services.MongoDbService()


def init_response():
    """
    Initialise the services used by the core framework.

    """
    Response()


def init_textsentiment():
    TextSentiment().train()


class Application(tornado.wsgi.WSGIApplication):
    def __init__(self, **kwars):
        handlers = [
            url(r"/", api.BaseHandler),
            url(r"/predict", api.PredictHandler),
            url(r"/login", api.LoginHandler), # done
            url(r"/register", api.RegisterHandler), # done
            url(r"/logout", api.LogoutHandler), # done
            url(r"/create_new_project", api.CreateProjectHandler), # done
            url(r"/get_projects", api.ProjectsHandler), # done
            url(r"/get_project/([\w]+)", api.ProjectHandler), # done
            url(r"/upload_data/([\w]+)", api.UploadDataHandler), # done
            url(r"/delete-data/([\w]+)/([\w]+)", api.DeleteDataByProjectDataHandler),#done
            url(r"/delete-data/([\w]+)", api.DeleteDataHandler), #done
            url(r"/datasets", api.RetrieveDataSetHandler), #done
            url(r"/load-project", api.SaveCurrentExperimentHandler), # done
            url(r"/experiments/([\w]+)", api.RetrieveExperimentsHandler),
            url(r"/results/([\w]+)", api.RetrieveResultsHandler),
            url(r"/add-data/([\w]+)/([\w]+)", api.AddDataToProjectDataHandler),
        ]

        settings = {
            'cookie_secret': self.gen_uniq_id(),
            'debug': False
            # 'autoreload': True
        }

        tornado.web.Application.__init__(self, handlers, **settings)
        self.syncconnection = MongoClient(MONGO_SERVER, 27017, connect=False)

        if 'db' in kwars:
            self.syncdb = self.syncconnection[kwars['db']]
        else:
            self.syncdb = self.syncconnection['flpke-db']

    def gen_uniq_id(self, num_bytes=16):
        return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    sockets = tornado.netutil.bind_sockets(options.port, address=options.address)
    # tornado.process.fork_processes(0) does not work on windows
    init_csvloader()
    init_regressors()
    init_classifiers()
    init_services()
    init_response()
    init_textsentiment()
    server = httpserver.HTTPServer(Application())
    server.add_sockets(sockets)

    print('Web server is listing at :' + options.address + ':' + str(options.port))
    tornado.ioloop.IOLoop.instance().start()
