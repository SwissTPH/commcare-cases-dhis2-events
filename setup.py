# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='commcare-cases-dhis2-events',
    version='0.1.0',
    description='Routinely extract cases from CommCareHQ and post them as events to DHIS2',
    author='Swiss Tropical and Public Health Institute (Swiss TPH)',
    author_email='david.huser@unibas.ch',
    url='https://github.com/SwissTPH/commcare-cases-dhis2-events',
    keywords='dhis2 commcare dimagi',
    install_requires=[
        'requests>=2.11.1',
        'python-dateutil>=2.5.3'
    ],
    packages=find_packages(),
    test_suite='pytest',
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)