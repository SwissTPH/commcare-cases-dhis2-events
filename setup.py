# -*- coding: utf-8 -*-
import os

from setuptools import setup

__version__ = ''
with open(os.path.join('app', 'version.py')) as f:
    exec (f.read())

setup(name='commcare-cases-dhis2-events',
      version=__version__,
      description='Routine ETL for CommCare cases --> DHIS2 events',
      author='Swiss Tropical and Public Health Institute (Swiss TPH)',
      author_email='david.huser@swisstph.ch',
      url='https://github.com/SwissTPH/commcare-cases-dhis2-events',
      packages=['app'],
      install_requires=[
          'requests>=2.11.1',
          'python-dateutil>=2.5.3',
          'pytest>=3.0.4',
          'pytest-cov>=2.4.0'
      ],
      test_suite='pytest',
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )
