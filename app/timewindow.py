import datetime
import json


class Timewindow:
    """ Handling Timewindow tuples of (start-string, end-string)"""

    def __init__(self, start, end):
        self.window = (start, end)

    def __getitem__(self, index):
        return self.window[index]

    def __len__(self):
        return len(self.window)

    def __repr__(self):
        return json.dumps(self.window)


def get_windows_from_start_to_end(start_ts, end_ts):
    """ creating a list of window strings from a starting date until the last full hour"""
    window_list = []
    time_format = '%Y-%m-%dT%H:%M:%S'
    index = start_ts
    while index < end_ts:
        s = index
        e = index + datetime.timedelta(hours=1, seconds=-1)
        minutes_diff = (end_ts - index).total_seconds() / 60.0
        if minutes_diff < 60.0:
            e = end_ts
        tw = Timewindow(start=s.strftime(time_format), end=e.strftime(time_format))
        window_list.append(tw)
        index = index + datetime.timedelta(hours=1)
    return window_list


def get_window_of_lasthour(datetimenow):
    """ timewindow strings of last hour, XX:00:00 - XX:59:59 where XX = NOW.hour-1 """
    before = (datetimenow - datetime.timedelta(hours=1))
    start = before.strftime("%Y-%m-%dT%H:00:00")
    end = before.strftime("%Y-%m-%dT%H:59:59")
    return Timewindow(start, end)
