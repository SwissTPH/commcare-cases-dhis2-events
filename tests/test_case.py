import pytest

from app.case import Case


@pytest.fixture
def case_with_orgunit():
    obj = {
        "case_id": "45WKYXQRFFU3AT4Y022EX7HF2",
        "date_closed": "2012-03-13T18:21:52Z",
        "properties": {
            "userLocationOrgUnitID": "NC3WdxGafv5",
            "prop1": 1,
            "prop2": 0,
            "prop3": True,
            "prop4": False,
            "prop5": None,
            "prop6": "1",
            "prop7": "0",
            "prop8": "foo",
            "prop9": 25,
            "prop10": "25",
            "prop11": "9.9",
            "prop12": 9.9
        }
    }
    return obj


@pytest.fixture
def case_without_orgunit():
    obj = {
        "case_id": "45WKYXQRFFU3AT4Y022EX7HF2",
        "date_closed": "2012-03-13T18:21:52Z",
        "properties": {
            "prop1": 1,
        }
    }
    return obj

@pytest.fixture
def case_with_unrecognized_property_valuetype():
    obj = {
        "case_id": "45WKYXQRFFU3AT4Y022EX7HF2",
        "date_closed": "2012-03-13T18:21:52Z",
        "properties": {
            "prop1":list(),
        }
    }
    return obj


def test_case_has_orgunit(case_with_orgunit):
    try:
        case = Case(case_with_orgunit)
        assert case.__getitem__('orgunit') == "NC3WdxGafv5"
    except ValueError:
        pass


def test_case_has_no_orgunit(case_without_orgunit):
    with pytest.raises(ValueError):
        Case(case_without_orgunit)


def test_property_is_true(case_with_orgunit):
    c = Case(case_with_orgunit)
    assert c.__getitem__('prop1') is True
    assert c.__getitem__('prop6') is True
    assert c.__getitem__('prop3') is True


def test_property_is_false(case_with_orgunit):
    c = Case(case_with_orgunit)
    assert c.__getitem__('prop2') is False
    assert c.__getitem__('prop4') is False
    assert c.__getitem__('prop7') is False


def test_property_is_none(case_with_orgunit):
    c = Case(case_with_orgunit)
    assert c.__getitem__('prop5') is None


def test_property_is_string(case_with_orgunit):
    c = Case(case_with_orgunit)
    assert c.__getitem__('prop8') == 'foo'
    assert c.__getitem__('prop9') == '25'
    assert c.__getitem__('prop10') == '25'
    assert c.__getitem__('prop11') == '9.9'
    assert c.__getitem__('prop12') == '9.9'

def test_property_valueerror(case_with_unrecognized_property_valuetype):
    with pytest.raises(ValueError):
        Case(case_with_unrecognized_property_valuetype)
