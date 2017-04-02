#!/usr/bin/env python

import argparse
from dateutil.parser import parse
import datetime


def parse_args(args):
    ap = argparse.ArgumentParser(description='Extract cases from CommCare and post as anonymous events to DHIS2')
    fromdate_help = 'Extract cases from this date until now, e.g. --fromdate 2016-06-30'
    window_help = 'Extract cases between two timestamps, e.g. --timewindow 2016-07-11T00:00:00 2016-07-11T23:59:59'
    dry_help = 'Dry-Run flag - Do not post to DHIS2, just save import file to ../logs/notposted'
    group = ap.add_mutually_exclusive_group()
    group.add_argument('-f', '--fromdate', action='store', metavar='DATE', nargs=1, help=fromdate_help)
    group.add_argument('-w', '--timewindow', action='store', metavar='TIMESTAMP', nargs=2, help=window_help)
    ap.add_argument('-d', '--dry', action='store_true', help=dry_help)
    ap.set_defaults(dry=False)

    arguments = ap.parse_args(args)

    if arguments.fromdate is not None:
        try:
            isinstance(parse(arguments.fromdate[0]), datetime.date)
        except ValueError:
            pass
            raise argparse.ArgumentError(None, 'Not a valid date string. See examples with run.py --help')
    elif arguments.timewindow is not None:
        for arg in arguments.timewindow:
            try:
                isinstance(parse(arg), datetime.date)
            except ValueError:
                pass
                raise argparse.ArgumentError(None, 'Not a valid date string. See examples with run.py --help')

        if parse(arguments.timewindow[0]) >= parse(arguments.timewindow[1]):
            raise argparse.ArgumentError(None, 'Start-timestamp is AFTER End-timestamp.')

    return arguments
