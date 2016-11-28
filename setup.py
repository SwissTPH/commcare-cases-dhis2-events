from setuptools import setup, find_packages

setup(name='commcare-cases-dhis2-events',
      version='0.1',
      description='Extract cases from CommCareHQ and post them as events to DHIS2',
      author='Swiss Tropical and Public Health Institute (Swiss TPH)',
      author_email='david.huser@unibas.ch',
      url='https://github.com/SwissTPH/commcare-cases-dhis2-events',
      packages=find_packages()
      )