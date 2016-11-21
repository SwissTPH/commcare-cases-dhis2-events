import pytest

from app.dhis import DhisHandler, transform_cases_to_events


def test_demo_server_200():
    dhis = DhisHandler(url='https://play.dhis2.org/demo/api/me.json', username='admin', password='district')
    response = dhis.get()
    assert response['email'] == 'someone@dhis2.org'


@pytest.fixture
def case_list():
    cases = [
        {
            "case_id": "45WKYXQRFFU3AT4Y022EX7HF2",
            "case_date": "2012-03-13",
            "orgunit": "NC3WdxGafv5",
            "someflag": False,
            "othervalue": None,
            "anotherone": "text",
            "lastone": 2
        }
    ]
    return cases


@pytest.fixture
def mapping():
    map = {
        "exclude": {
            "dontwantthisposted": "badfaef",
        },
        "include": {
            "someflag": "hs3Wugcy4mt",
            "othervalue": "ju82ugJy7ut",
            "anotherone": "abc20daleld",
            "lastone": "ekfi2kdhfei"
        }
    }
    return map


def test_transform_cases_to_events(case_list, mapping):
    program = 'qq3Wu3gy4mt'
    username = 'admin'

    events = transform_cases_to_events(case_list=case_list, mapping=mapping, program=program, username=username)

    assert len(events) == 1
    assert len(events['events']) == 1

    expected_dv = [
        {'dataElement': 'hs3Wugcy4mt', 'value': False},
        {'dataElement': 'abc20daleld', 'value': 'text'},
        {'dataElement': 'ekfi2kdhfei', 'value': 2}
    ]

    print events['events'][0]['dataValues']

    assert events['events'][0]['program'] == program
    assert events['events'][0]['storedBy'] == username
    assert events['events'][0]['eventDate'] == '2012-03-13'
    assert any(map(lambda v: v in events['events'][0]['dataValues'], expected_dv))
    assert len(events['events'][0]['dataValues']) == 3
    assert events['events'][0]['orgUnit'] == 'NC3WdxGafv5'
