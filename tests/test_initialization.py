import json
import os

import pytest

from app.helpers.filehandler import read_json, store_events, find


def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


@pytest.fixture()
def config_file():
    content = {

        "commcare": {
            "url": "https://example.commcarehq.org/a/icrc-almanach/api/v0.5/case/",
            "username": "commcare-username",
            "password": "commcare-password",
            "case_type": "CC_Case_Type",
            "cert": "mysslcertificate.crt.pem"
        },
        "dhis2": {
            "url": "https://play.dhis2.org/demo/api/events",
            "username": "admin",
            "password": "district",
            "program": "UID-of-program-without-registration"
        },
        "log": {
            "fileloglevel": "logging.DEBUG",
            "mailloglevel": "logging.ERROR"
        },
        "mail": {
            "host": "smtp.gmail.com",
            "from": "example@gmail.com",
            "to": [
                "me@company.com",
                "othermailbox@company.com"
            ],
            "subject": "[COMMCARE->DHIS2] Error",
            "username": "example@gmail.com",
            "password": "smtp-password"
        }
    }
    # write file to repository root
    filename = 'config_test.json'
    with open(filename, 'w') as f:
        json.dump(content, f)
    return filename


def test_read_config(config_file):
    c = read_json(config_file)
    assert len(c) == 4
    assert c['commcare']['url'] == 'https://example.commcarehq.org/a/icrc-almanach/api/v0.5/case/'

    # remove file from repository root
    root_dir = os.path.dirname(os.path.abspath(__file__))[:-6]
    filename = os.path.join(root_dir, config_file)
    os.remove(filename)


@pytest.fixture()
def events():
    events = {
        "events": [
            {
                "program": "eBAyeGv0exc",
                "orgUnit": "DiszpKrYNg8",
                "eventDate": "2013-05-17",
                "status": "COMPLETED",
                "storedBy": "admin",
                "coordinate": {
                    "latitude": "59.8",
                    "longitude": "10.9"
                },
                "dataValues": [
                    {"dataElement": "qrur9Dvnyt5", "value": "22"},
                    {"dataElement": "oZg33kd9taw", "value": "Male"}
                ]},
            {
                "program": "eBAyeGv0exc",
                "orgUnit": "DiszpKrYNg8",
                "eventDate": "2013-05-17",
                "status": "COMPLETED",
                "storedBy": "admin",
                "coordinate": {
                    "latitude": "59.8",
                    "longitude": "10.9"
                },
                "dataValues": [
                    {"dataElement": "qrur9Dvnyt5", "value": "26"},
                    {"dataElement": "oZg33kd9taw", "value": "Female"}
                ]}
        ]
    }
    return events


def test_store_events(tmpdir, events):
    starttime = '2010-09-03T00-00-00Z'
    endtime = '2010-09-03T23-59-59Z'
    p = tmpdir.mkdir("mydir").join("{}_{}.json".format(starttime, endtime))
    p.write(json.dumps(events))
    assert p.read() == json.dumps(events)

def test_find_file():
    assert find('LICENSE.txt')
    assert find('README.md')


def test_not_find_file():
    with pytest.raises(IOError) as e:
        find("notexistent.txt")
