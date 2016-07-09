***********
Backend-api
***********

Upload dataset(csv) select features and labels, train your your model and then predict.


Supported Algorithms
====================


Regression
----------

* LinearRegression
* Svm Linear Regression
* Decision Tree Regression
* Random Forest Regression


Classifiers
-----------

* SGD Classifier
* KNeighborsClassifier
* Svm Classifier
* Decision Tree Classifier
* Random Forest Classifier
* Ada Boost Classifier
* Gaussian Nb Classifier
* Linear Discriminant Analysis Classifier
* Quadratic Discriminant Analysiscls Classifier

* Sentiment-Analysis


Environment setup
=================

Following instruction are for those who want to use venv, if you running this project globally then skip the venv setup and install the required dependencies by using pip.


Python3
-------

It is highly recommended to run everything in an up-to-date virtualenv.
The environment can be set up using:

.. code-block:: sh

    $ export VENV=/tmp/venv-$RANDOM
    $ virtualenv $VENV
    $ source $VENV/bin/activate
    $ pip install pip --upgrade
    $ pip install setuptools --upgrade


Next install this project using ``pip``::

    $ pip install -e .


Database
========

This project is using mongobd as databse. Install and run mongodb in order to run
this project.y

Run Program
===========
Navigate to the root directory of the project and hit:
    
    $ python src/main.py

Build Api documentaion
======================

Navigate to the doc folder.


Running the build

$ sphinx-build -b html sourced build


Makefile

$ make html

Documnetation will be available inside
  ``doc/build/html/index.html``
