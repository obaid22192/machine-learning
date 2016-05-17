from setuptools import find_packages
from setuptools import setup


setup(
    name='model-prediction',
    version='0.0.1',
    include_package_data=True,
    author='team-tree',
    description='Sales prediction api.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'tornado',
        'syringe',
        'bcrypt',
        'pymongo',
        'textblob',
        'mongoengine',
        'Sphinx'
    ],
    zip_safe=True)
