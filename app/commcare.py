#!/usr/bin/env python
"""
CommcareHandler API object
calls the API with a GET request with specified parameters
"""
import json

import requests

try:
    from helpers.logger import *
except ImportError:
    from app.helpers.logger import *


class CommcareHandler(object):
    """ Base class for accessing Commcare API"""

    def __init__(self, url, username, password, case_type, ssl_cert=None):
        self.url = url
        self.username = username
        self.password = password
        self.case_type = case_type
        self.ssl_cert = ssl_cert

        if not any([self.url, self.username, self.password, self.case_type]):
            raise ValueError("Empty credentials", self.username, self.case_type, self.url)

        if not self.url.endswith('/case/'):
            raise ValueError("Check Commcare API URL, must end with '/case/'")

    def get(self, starttime, endtime):
        """ GET closed cases from Commcare with payload (timewindow) and (case_type)"""
        payload = {
            'server_date_modified_start': starttime,
            'server_date_modified_end': endtime,
            'type': self.case_type,
            'closed': True,
            'limit': 100
        }

        log_debug("Commcare request: {}".format(json.dumps(payload)))
        try:
            req = requests.get(self.url, auth=(self.username, self.password), params=payload, verify=self.ssl_cert)
            log_debug("{} CommCare response: {}".format(self.url, req.text))
            if req.status_code == 200:
                return req.json()
            else:
                log_error("Commcare error occured: {}".format(req.text))
        except requests.RequestException as e:
            log_error(e)

    @staticmethod
    def cases_available(response):
        """ Check if response contains actual content to process"""
        if response:
            no_of_objects = response['meta']['total_count']
            if no_of_objects > 0:
                print("{} cases fetched".format(str(no_of_objects)))
                return True

        log_info("No cases to fetch.")
        return False
