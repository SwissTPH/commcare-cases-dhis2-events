from setuptools import setup, find_packages

_VERSION_ = '0.1'

setup(name='commcare-cases-dhis2-events',
      version=_VERSION_,
      description='Extract cases from CommCareHQ and post them as events to DHIS2',
      author='Swiss Tropical and Public Health Institute (Swiss TPH)',
      author_email='david.huser@unibas.ch',
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
