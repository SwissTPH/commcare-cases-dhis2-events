#!/usr/bin/env python

import json
import os


def find(name, root_dir=os.path.dirname(os.path.abspath(__file__))):
    """Find path of a file in the repository's directory"""
    root_dir = root_dir[:-12]
    if root_dir:
        for root, dirs, files in os.walk(root_dir):
            if name in files:
                return os.path.join(root, name)
            else:
                raise IOError


def read_json(filename):
    """ find and read content from JSON file"""
    path = find(filename)
    with open(path, 'r') as json_file:
        content = json.load(json_file)
        if content is None:
            raise IOError('Config file is empty.')
    return content


def store_events(events, starttime, endtime):
    """Dump DHIS2 events into json file"""
    root_dir = os.path.dirname(os.path.abspath(__file__))[:-12]
    file_name = 'events_{}_{}.json'.format(starttime.replace(":", "-"), endtime.replace(":", "-"))
    events_path = os.path.join(root_dir, 'logs', 'notposted', file_name)

    with open(events_path, 'w') as f:
        json.dump(events, f, indent=4)

    return events_path


def remove_file(path):
    """Delete file"""
    os.remove(path)


def create_folders():
    """create folders for logs and event dump if they do not exist yet"""
    root_dir = os.path.dirname(os.path.abspath(__file__))[:-12]
    log_path = os.path.join(root_dir, 'logs')
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    events_path = os.path.join(root_dir, 'logs', 'notposted')
    if not os.path.isdir(events_path):
        os.makedirs(events_path)
