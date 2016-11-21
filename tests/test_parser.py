from app.helpers.argparser import parse_args

import argparse
import pytest

def test_parser_fromdate():
    parser = parse_args(['--fromdate', '2016-06-30'])
    assert parser.fromdate[0] == '2016-06-30'


def test_parser_timewindow():
    parser = parse_args(['--timewindow', '2016-07-11T00:00:00', '2016-07-11T23:59:59'])
    assert parser.timewindow[0] == '2016-07-11T00:00:00'
    assert parser.timewindow[1] == '2016-07-11T23:59:59'

def test_parser_timewindow_wrong():
    with pytest.raises(argparse.ArgumentError):
        parse_args(['--timewindow', '2016-07-11XXX', '2016-x1T23:59:59'])

def test_parser_timewindow_start_after_end():
    parser = parse_args(['--timewindow', '2015-12-31', '2016-01-01'])
    assert parser.timewindow[0] < parser.timewindow[1]
    with pytest.raises(argparse.ArgumentError):
        parse_args(['--timewindow', '2016-01-01', '2015-12-31'])


def test_parser_dryrun():
    parser = parse_args(['--dry'])
    assert parser.dry is True


def test_parser_no_arguments():
    parser = parse_args([])
    assert parser.dry is False
    assert parser.fromdate is None
    assert parser.timewindow is None
