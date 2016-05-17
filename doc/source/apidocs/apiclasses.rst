############
Register:
############


********
Request:
********


   **Example request**:
   *register*

   .. sourcecode:: http

      Request URL: POST apiurl/register  HTTP/1.1
      Host: apiurl


********
Response:
********

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

   :form email: user email address
   :form password: password
   :statuscode 200: success
   :statuscode 404: there's no registration

############
Login:
############

********
Request:
********


   **Example request**:
   *login*

   .. sourcecode:: http

      Request URL: POST apiurl/login  HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

   :form email: user email address
   :form password: password
   :statuscode 200: no error
   :statuscode 304: login with email address
   :statuscode 404: there's no user


###################
Create new project:
###################


********
Request:
********


   **Example request**:
   *Create new project*

   .. sourcecode:: http

      Request URL: POST apiurl/create_new_project HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        "project_creation_date": "2016-01-24T21:59:14.294756",
        "project_name": "new project",
        "user_id": "568eb497a226653a2bcaef25",
        "project_id": "56a53b22a22665465dc11106"
      }

   :form project_name: new project
   :statuscode 200: no error
   :statuscode 304: login with email address
   :statuscode 404: there's no user



#############
Get projects:
#############


********
Request:
********

   **Example request**:
   **Get all projects belongs to current user*

   .. sourcecode:: http

      Request URL: GET apiurl/get_projects HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      [
         {
             "project_name": "Project_1",
             "project_creation_date": "2016-01-13T08:21:44.114000",
             "project_id": "5695fb082a45ab5ed0c3bc83",
             "user_id": "5695f5662a45ab5ed0c3bb94"
         },
         {
             "project_name": "Project_12",
             "project_creation_date": "2016-01-13T08:21:44.114000",
             "project_id": "5695fb082a45ab5ed0c3bc83",
             "user_id": "5695f5662a45ab5ed0c3bb94"
         }
      ]

   :statuscode 200: no error
   :statuscode 405: there's no user


#############
Get project:
#############


********
Request:
********

   **Example request**:
   *Get project by its ID*

   .. sourcecode:: http

      Request URL: GET apiurl/get_project/projectId HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      {
         "project_name": "Project_1",
         "project_creation_date": "2016-01-13T08:21:44.114000",
         "project_id": "5695fb082a45ab5ed0c3bc83",
         "user_id": "5695f5662a45ab5ed0c3bb94"
      }


   :statuscode 200: no error
   :statuscode 405: there's no user


################
Upload data set:
################


********
Request:
********

   **Example request**:

   .. sourcecode:: http

      Request URL: POST apiurl/upload_data/projectID HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      {
         "data_set_id": "56a5412ea2266546a5229988",
         "dataset_columns": [
            "column name 1",
            "column name 2"
          ],
         "project_id": "5695fb082a45ab5ed0c3bc83",
         "user_id": "5695f5662a45ab5ed0c3bb94",
         "dataset_id": ""568eb497a226653a2bcaef255698cf86a226656534c6119ba",
         "project_id": [
            "5698cf86a226656534c6119b"
         ],
         "user_id": "568eb497a226653a2bcaef25"
      }

   :query string body: file
   :statuscode 200: no error
   :statuscode 405: there's no user
   :statuscode 401: unauthourised


############################
Delete data by from project:
############################


********
Request:
********

   **Example request**:

   .. sourcecode:: http

      Request URL: GET apiurl/upload_data/projectID/datasetID HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

   :query string body: file
   :statuscode 200: no error
   :statuscode 405: there's no user
   :statuscode 401: unauthourised


############################
Delete dataset from databse:
############################


********
Request:
********

   **Example request**:

   .. sourcecode:: http

      Request URL: GET apiurl/upload_data/datasetID HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

   :query string body: file
   :statuscode 200: no error
   :statuscode 405: there's no user
   :statuscode 401: unauthourised


####################################
Retrieve datasets for currennt user:
####################################


********
Request:
********

   **Example request**:

   .. sourcecode:: http

      Request URL: GET apiurl/datasets HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      [
        {
           "data_set_id": "56a5412ea2266546a5229988",
           "dataset_columns": [
              "column name 1",
              "column name 2"
            ],
           "project_id": "5695fb082a45ab5ed0c3bc83",
           "user_id": "5695f5662a45ab5ed0c3bb94",
           "dataset_id": ""568eb497a226653a2bcaef255698cf86a226656534c6119ba",
           "project_id": [
              "5698cf86a226656534c6119b"
           ],
           "user_id": "568eb497a226653a2bcaef25"
        },
        {
         "data_set_id": "56a5412ea2266546a5229988",
         "dataset_columns": [
            "column name 1",
            "column name 2"
          ],
         "project_id": "5695fb082a45ab5ed0c3bc83",
         "user_id": "5695f5662a45ab5ed0c3bb94",
         "dataset_id": ""568eb497a226653a2bcaef255698cf86a226656534c6119ba",
         "project_id": [
            "5698cf86a226656534c6119b"
         ],
         "user_id": "568eb497a226653a2bcaef25"
        }
      ]

   :query string body: file
   :statuscode 200: no error
   :statuscode 405: there's no user
   :statuscode 401: unauthourised


####################
Load new experiment:
####################


********
Request:
********

   **Example request**:

   .. sourcecode:: http

      Request URL: POST apiurl/load-project HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      {
        'project_id': '5698cf86a226656534c6119b',
        'algorithms': [
          'LinearRegression',
          'Random Forest Regression',
          'Decision Tree Regression',
          'Svm Linear Regression'
        ],
        'test_size': 11,
        'labels': [
          {
            "lable":"ORD_TOTALAMOUNTINC",
            "dataset":"56a5412ea2266546a5229988"
          }
        ],
        'features':
          [
            {
              "feature":"Number_of_cus",
              "dataset":"56a5412ea2266546a5229988"
            },
            {
              "feature":"Month",
              "dataset":"56a5412ea2266546a5229988"
            },
            {
              "feature":"Paper_con_value",
              "dataset":"56a5412ea2266546a5229988"
            }
          ]
      }

   :query string body: {
                        'project_id': '5698cf86a226656534c6119b',
                        'algorithms': [
                          'LinearRegression',
                          'Random Forest Regression',
                          'Decision Tree Regression',
                          'Svm Linear Regression'
                        ],
                        'test_size': 11,
                        'labels': [
                          {
                            "lable":"ORD_TOTALAMOUNTINC",
                            "dataset":"56a5412ea2266546a5229988"
                          }
                        ],
                        'features':
                          [
                            {
                              "feature":"Number_of_cus",
                              "dataset":"56a5412ea2266546a5229988"
                            },
                            {
                              "feature":"Month",
                              "dataset":"56a5412ea2266546a5229988"
                            },
                            {
                              "feature":"Paper_con_value",
                              "dataset":"56a5412ea2266546a5229988"
                            }
                          ]
                      }

   :statuscode 200: no error
   :statuscode 405: there's no user
   :statuscode 401: unauthourised


####################
GET all  experiment:
####################


********
Request:
********

   **Example request**:

   .. sourcecode:: http

      Request URL: GET apiurl/experiments/projectID HTTP/1.1
      Host: apiurl

********
Response:
********


   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      [
        {
          'creation_timestamp': "2016-01-22T10:18:47.110000"
          'project_id': '5698cf86a226656534c6119b',
          'algorithms': [
            'LinearRegression',
            'Random Forest Regression',
            'Decision Tree Regression',
            'Svm Linear Regression'
          ],
          'test_size': 11,
          'labels': [
            {
              "lable":"ORD_TOTALAMOUNTINC",
              "dataset":"56a5412ea2266546a5229988"
            }
          ],
          'features':
            [
              {
                "feature":"Number_of_cus",
                "dataset":"56a5412ea2266546a5229988"
              },
              {
                "feature":"Month",
                "dataset":"56a5412ea2266546a5229988"
              },
              {
                "feature":"Paper_con_value",
                "dataset":"56a5412ea2266546a5229988"
              }
            ]
        }
      ]


   :statuscode 200: no error
   :statuscode 405: there's no user
   :statuscode 401: unauthourised
