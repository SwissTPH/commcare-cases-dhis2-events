#!/usr/bin/env python

import time
from dateutil import parser

from case import Case
from commcare import CommcareHandler
from dhis import DhisHandler, transform_cases_to_events
from helpers.argparser import parse_args
from helpers.config import Configuration, install_mapping
from helpers.filehandler import find, store_events, remove_file, create_folders, read_json
from helpers.logger import *
from version import __version__
from timewindow import *


def case_factory(commcare, timewindows):
    case_list = []
    no_of_tw = len(timewindows)
    if no_of_tw > 1:
        print("Number of CommCare calls: {}".format(no_of_tw))
        print("Estimated time to complete: {} min".format(round(1.6 * no_of_tw / 60, 0)))

    for i, (starttime, endtime) in enumerate(timewindows):
        time.sleep(0.5)
        print("{} - {}".format(starttime, endtime))
        response = commcare.get(starttime, endtime)
        if commcare.cases_available(response):
            for obj in response['objects']:
                try:
                    case = Case(obj)
                    case_list.append(case)
                except ValueError as e:
                    log_error(e)

    return case_list


def main():
    """ START """
    root_dir = os.path.abspath(os.path.dirname(__file__))[:-4]
    config = Configuration()
    create_folders()
    init_logger(config)
    install_mapping(root_dir)

    mapping = read_json('mapping.json')

    # find SSL certificate repository root directory
    ssl_cert = None
    try:
        ssl_cert = find(config['commcare']['cert'])
    except IOError:
        pass

    print("---\nCommcare cases to DHIS2 events V. {}\n".format(__version__))
    print("CommCare: {} @ {}\n DHIS2 URL: {} @ {}\n".format(config['commcare']['username'], config['commcare']['url'],
                                                            config['dhis2']['username'], config['dhis2']['url']))
    # parse arguments
    args = parse_args(sys.argv[1:])

    commcare = CommcareHandler(
        config['commcare']['url'],
        config['commcare']['username'],
        config['commcare']['password'],
        config['commcare']['case_type'],
        ssl_cert
    )

    case_list = []
    now = datetime.datetime.now()

    # ******** FROMDATE MODE *********
    if args.fromdate:
        log_info("Running in FROMDATE mode.")
        start_date = parser.parse(timestr=args.fromdate[0])
        start_datetime = datetime.datetime(year=start_date.year, month=start_date.month, day=start_date.day, hour=0,
                                           minute=0, second=0)
        timewindows = get_windows_from_start_to_end(start_datetime, now)

        case_list = case_factory(commcare, timewindows)

        # for filename only:
        file_start = start_datetime.strftime('%Y-%m-%dT%H-%M-%S')
        file_end = now.strftime('%Y-%m-%dT%H-%M-%S')

    # ******** WINDOW MODE *********
    elif args.timewindow:
        log_info("Running in WINDOW mode.")
        start_datetime = parser.parse(timestr=args.timewindow[0])
        end_datetime = parser.parse(args.timewindow[1])
        timewindows = get_windows_from_start_to_end(start_datetime, end_datetime)

        case_list = case_factory(commcare, timewindows)

        # for filename only:
        file_start = start_datetime.strftime('%Y-%m-%dT%H-%M-%S')
        file_end = end_datetime.strftime('%Y-%m-%dT%H-%M-%S')

    # ******** ROUTINE / CRONJOB MODE *********
    else:
        # example: now = 09:45:23 -> rounded_down = 09:00:00
        rounded_down = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=0, second=0)
        # subtract one hour
        last_hour = rounded_down - datetime.timedelta(hours=1)
        last_hour_5959 = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour - 1, minute=59,
                                           second=59)
        timewindow = get_windows_from_start_to_end(start_ts=last_hour, end_ts=last_hour_5959)

        case_list = case_factory(commcare, timewindow)

        # for filename only:
        file_start = last_hour.strftime('%Y-%m-%dT%H-%M-%S')
        file_end = last_hour_5959.strftime('%Y-%m-%dT%H-%M-%S')

    events = transform_cases_to_events(case_list=case_list, mapping=mapping, program=config['dhis2']['program'],
                                       username=config['dhis2']['username'])
    no_of_events = len(events['events'])
    if no_of_events > 0:
        file_path = store_events(events, file_start, file_end)
        dhis = DhisHandler(
            config['dhis2']['url'],
            config['dhis2']['username'],
            config['dhis2']['password']
        )
        log_info("Created {} DHIS2 events... ".format(str(no_of_events)))

        if not args.dry:
            if no_of_events > 0:
                success = dhis.post(events)
                if success:
                    remove_file(file_path)
        else:
            log_info("Events were not posted to DHIS2 (Dry-Run Mode) but import file was stored at {}".format(
                os.path.join(root_dir, 'logs', 'notposted')))


if __name__ == '__main__':
    main()
