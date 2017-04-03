import pytest

from app.helpers.config import *


@pytest.fixture()
def config_file():
    csv_file = [
        'commcare_id;dhis2_id;filter',
        'ageInYears;wiiDcsQ5pdQ;INCLUDE',
        'gender;RsZ4gQzWPWU;INCLUDE',
        'weight;L7aO70bcrbP;INCLUDE',
        'feverFlag;x1708y0C4C7;INCLUDE',
        'case_type;;EXCLUDE',
        'childHeight;;EXCLUDE',
        'date_opened;;EXCLUDE',
        'patientToken;;EXCLUDE',
        'severeAcuteMalnutritionFlag;;EXCLUDE',
        'vitaminALast6Months;;EXCLUDE'
    ]

    path = 'config_test.csv'
    import csv
    with open(path, 'w') as f:
        w = csv.writer(f, delimiter=';')
        w.writerows([x.split(';') for x in csv_file])
    return path


def test_parse_id_filter(config_file):
    try:
        out = parse_id_filter(config_file)
        assert len(out) == 2
        assert len(out['include']) == 4
        assert len(out['exclude']) == 6
        assert out['include'].get('ageInYears', None) == 'wiiDcsQ5pdQ'
        assert out['include'].get('childHeight', None) is None
        assert out['exclude'].get('childHeight', None) == ''
    finally:
        import os
        # remove file from repository root
        root_dir = os.path.dirname(os.path.abspath(__file__))[:-6]
        filename = os.path.join(root_dir, config_file)
        os.remove(filename)
