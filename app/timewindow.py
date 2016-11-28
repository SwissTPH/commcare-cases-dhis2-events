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


def create_timewindow(start, end):
    """
    creating tuples with starttime and endtime. Input is day and hour, eg. <2016-03-03> and <15>
    Example return: (2016-03-03T15:00:00Z, 2016-03-03T15:59:59Z)
    """
    s = "{}T{}".format(start.strftime("%Y-%m-%d"), start.strftime("%H:%M:%S"))
    e = "{}T{}".format(end.strftime("%Y-%m-%d"), end.strftime("%H:%M:%S"))
    return Timewindow(s, e)


def get_windows_from_start_to_end(start_ts, end_ts):
    """ creating a list of window strings from a starting date until the last full hour"""
    window_list = []
    index = start_ts
    while index < end_ts:
        s = index
        e = index + datetime.timedelta(hours=1, seconds=-1)
        minutes_diff = (end_ts - index).total_seconds() / 60.0
        if minutes_diff < 60.0:
            e = end_ts
        tw = create_timewindow(s, e)
        window_list.append(tw)
        index = index + datetime.timedelta(hours=1)
    return window_list


def get_window_of_lasthour(datetimenow):
    """ timewindow strings of last hour, XX:00:00 - XX:59:59 where XX = NOW.hour-1 """
    # round <now> down to the full hour minus 1 second, strip to XX:59:59 format
    last_hour_fiftynine_fiftynine = str(datetimenow - datetime.timedelta(minutes=datetimenow.minute,
                                                                         seconds=datetimenow.second + 1,
                                                                         microseconds=datetimenow.microsecond))[11:]
    # subtract one hour from now, round down to the full hour, strip to XX:00:00 format
    last_hour_zerozero = str(datetimenow - datetime.timedelta(minutes=datetimenow.minute + 60,
                                                              seconds=datetimenow.second,
                                                              microseconds=datetimenow.microsecond))[11:]

    # add T and Z in between
    date_today = datetimenow.strftime("%Y-%m-%d")
    start = date_today + "T" + last_hour_zerozero + "Z"
    end = date_today + "T" + last_hour_fiftynine_fiftynine + "Z"
    window = Timewindow(start, end)
    return window
