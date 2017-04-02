#!/usr/bin/env python

import csv
import json
import os
import sys

from .filehandler import find


class Configuration(object):
    def __init__(self):
        # find config file and store it
        path = find('config.json')
        with open(path) as json_config_file:
            self.config = json.load(json_config_file)

    def __getitem__(self, item):
        return self.config[item]


def install_mapping(path):
    """find config CSV, read and store it as JSON """
    installed = False
    try:
        installed = find('mapping.json')
    except IOError:
        print("Will install mapping now...")
        pass
    if not installed:
        try:
            csv_file = find('mapping.csv')
            out = parse_id_filter(csv_file)

            with open(os.path.join(path, 'mapping.json'), 'w') as f2:
                json.dump(out, f2, indent=4, sort_keys=True)

        except (IOError, KeyError) as e:
            print("No valid mapping.csv file found. Delimiter must be ';' and at least one ID must be INCLUDEd")
            print(e.args)
            sys.exit()


def parse_id_filter(csv_file):
    """ parse mapping file what IDs to include in config for sending to DHIS2"""
    out = {
        "include": {},
        "exclude": {}
    }
    with open(csv_file) as f1:
        reader = csv.DictReader(f1, delimiter=";")
        for row in reader:
            if row['filter'].lower() == 'include':
                out['include'][row['commcare_id']] = row['dhis2_id']
            else:
                out['exclude'][row['commcare_id']] = row['dhis2_id']
    if len(out['include']) < 1:
        raise IOError
    return out
