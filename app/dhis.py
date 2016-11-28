#!/usr/bin/env python
"""
DHIS2 API object
calls the API with a post request with specified parameters
returns DHIS2 response and the HTTP status code
"""
import json

import requests

from helpers.logger import *


class DhisHandler:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    # POSTs events in JSON format to DHIS2 API (api/events endpoint)
    def post(self, events):
        headers = {'Content-Type': 'application/json'}

        try:
            req = requests.post(self.url, auth=(self.username, self.password), headers=headers,
                                data=json.dumps(events))
            log_info(req.text)
            if req.status_code != 200:
                log_error(req.text)
        except requests.RequestException as e:
            log_error(e)

    def get(self):
        try:
            req = requests.get(self.url, auth=(self.username, self.password))
            if req.status_code == 200:
                return req.json()
            else:
                return req.text
        except requests.RequestException as e:
            print(e)


def transform_cases_to_events(case_list, mapping, program, username):
    """ Transforms a list of Case objects into DHIS2 compliant events."""
    events = []
    ignored_values = {'null', '', None}
    for case in case_list:
        data_values = []
        for key, value in case.items():
            # check if data element should be included
            dhis2_id = mapping['include'].get(key, None)
            # check if value is not empty / 'null' / None
            if dhis2_id and value not in ignored_values:
                data_value_elem = {
                    'dataElement': dhis2_id,
                    'value': value
                }
                data_values.append(data_value_elem)

        event = {
            'program': program,
            'orgUnit': case['orgunit'],
            'eventDate': case['case_date'],
            'storedBy': username,
            'status': 'COMPLETED',
            'dataValues': data_values
        }
        events.append(event)
    # pack them to one object because DHIS2 requires it
    packaged = {'events': events}
    return packaged
