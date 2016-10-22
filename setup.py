import sys
from setuptools import setup, find_packages

__version__ = None
execfile('site/common/__init__.py') # Get __version__

if __version__ is None:
    raise RuntimeError('__version__ not found')

setup(
    name='payments',
    version=__version__,
    description='Payment website',
    url='https://github.com/pj2/payment-app',
    author='Joshua Prendergast',
    packages=find_packages(),
    install_requires=[
        'Django==1.10.2',
        'setuptools_scm',
        'mock',
        'pytest',
        'pytest-django',
        'pytest-pythonpath',
        'pytest-xdist',
    ],
)
