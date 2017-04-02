import pytest

from app.timewindow import *

# ---------------
FAKE_START_1 = datetime.datetime(2016, 9, 2, 0, 0)
FAKE_NOW_1 = datetime.datetime(2016, 9, 3, 23, 50, 00)


@pytest.fixture
def faked_now_1(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_NOW_1

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_get_all_windows_from_date_1(faked_now_1):
    now = datetime.datetime.now()
    windows = get_windows_from_start_to_end(start_ts=FAKE_START_1, end_ts=FAKE_NOW_1)
    assert now is FAKE_NOW_1
    # there should be 24 windows with each start- and endttime
    assert len(windows) == 2 * 24
    # check if windows contain really 2 per element
    assert len(windows[0]) == 2
    assert len(windows[-1]) == 2
    # check if last timestamp = end of last hour
    assert windows[-1][1] == '2016-09-03T23:50:00'


# ---------------
FAKE_START_2 = datetime.datetime(2015, 1, 1, 0, 0)
FAKE_NOW_2 = datetime.datetime(2015, 1, 31, 23, 30, 00)


@pytest.fixture
def faked_now_2(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_NOW_2

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_get_all_windows_from_date_2(faked_now_2):
    now = datetime.datetime.now()
    windows = get_windows_from_start_to_end(start_ts=FAKE_START_2, end_ts=FAKE_NOW_2)
    assert now is FAKE_NOW_2
    # 31 days * 24 hours
    assert len(windows) == 31 * 24
    # check if windows contain really 2 per element
    assert len(windows[0]) == 2
    assert len(windows[-1]) == 2
    # check if last timestamp = end of last hour
    assert windows[-1][1] == '2015-01-31T23:30:00'


# ---------------
FAKE_START_3 = datetime.datetime(2014, 12, 31, 23, 0, 0)
FAKE_NOW_3 = datetime.datetime(2015, 1, 1, 1, 30, 22)


@pytest.fixture
def faked_now_3(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_NOW_3

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_get_all_windows_from_date_3(faked_now_3):
    now = datetime.datetime.now()
    windows = get_windows_from_start_to_end(start_ts=FAKE_START_3, end_ts=FAKE_NOW_3)
    assert now is FAKE_NOW_3
    assert len(windows) == 3
    # check if windows contain really 2 per element
    assert len(windows[0]) == 2
    assert len(windows[-1]) == 2
    # check if last timestamp = end of last hour
    assert windows[-1][1] == '2015-01-01T01:30:22'


# ---------------
FAKE_START_4 = datetime.datetime(2015, 1, 1, 0, 0, 0)


def test_no_window_when_start_equal_end():
    windows = get_windows_from_start_to_end(start_ts=FAKE_START_4, end_ts=FAKE_START_4)
    assert len(windows) == 0


# ---------------
FAKE_NOW_5 = datetime.datetime(2016, 9, 3, 2, 0, 1)


@pytest.fixture
def faked_now_5(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_NOW_5

    monkeypatch.setattr(datetime, 'datetime', mydatetime)

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_get_window_of_last_hour():
    window = get_window_of_lasthour(FAKE_NOW_5)
    assert window[0] == "2016-09-03T01:00:00"
    assert window[1] == "2016-09-03T01:59:59"


def test_get_window_of_last_hour_midnight():
    FAKE_NOW_6 = datetime.datetime(2017, 4, 1, 0, 0, 0)
    window = get_window_of_lasthour(FAKE_NOW_6)
    assert window[0] == "2017-03-31T23:00:00"
    assert window[1] == "2017-03-31T23:59:59"
