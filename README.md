# CommCare Cases to DHIS2 Events

[![Build Status](https://travis-ci.org/SwissTPH/commcare-cases-dhis2-events.svg?branch=master)](https://travis-ci.org/SwissTPH/commcare-cases-dhis2-events)

Extract cases from [CommCare](https://www.commcarehq.org/home/) hourly and post them as anonymous events to [DHIS 2](https://www.dhis2.org). Store import failures as JSON files and report errors via mail.

## Installation

It is recommended to use Python 3 or Python>=2.7.9 due to various [SSL support warnings of urllib3](https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings). Both Python versions are supported though.

Install python3 and pip (if not already), virtualenv and dependencies:

- `sudo apt-get install python3-pip`
- `virtualenv env`
- `virtualenv -p python3 env`
- `source env/bin/activate`
- `git clone https://github.com/SwissTPH/commcare-cases-dhis2-events`
- `cd commcare-cases-dhis2-events`
- `python3 setup.py install`
- `python3 -m pytest tests` to see if everything is working.

## Configuration

- There are two important files: `config-template.json` which manages credentials and `mapping-template.csv` which manages the mapping of IDs between Commcare and DHIS2. 
- In `config-template.json`, edit the fields (especially `commcare`, `dhis2` and `mail`) and **save** as `config.json`.
- Restrict access to the file: `$ chmod 0600 config.json`
- In CommCare, each case needs a property `userLocationOrgUnitID` which contains the DHIS2 Organisation Unit UID where the Case took place. For other identifiers, check the DHIS2 API docs.
- Run the tests: `python setup.py test` to see if everything is working.

### Mapping file

In `mapping-template.csv`, there are 3 columns:

![mapping.csv](https://i.imgur.com/6XqEVqr.png)

- `commcare_id`: the Commcare case property name. Commcare API: [List Cases (version 3+)](https://confluence.dimagi.com/pages/viewpage.action?pageId=12224287)
- `dhis2_id`: The dataElement UID of DHIS2. DHIS2 API: [Sending events](https://dhis2.github.io/dhis2-docs/master/en/developer/html/webapi_events.html)
- `filter`: Maybe there are Commcare properties that should not be sent to DHIS2, in this case put `EXCLUDE` in this column, `INCLUDE` otherwise. It's best to inspect the CommCare response for this.
- Note that the CSV file must be delimited with `;` and **saved** as `mapping.csv`

## Usage

There are different modes in how you can interact with this connector.

```
$ python app/run.py --help
usage: run.py [-h] [-f DATE | -w TIMESTAMP TIMESTAMP] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -f or --fromdate DATE
                        Extract cases from this date until now, e.g. --fromdate 2016-06-30
  -w or --timewindow TIMESTAMP TIMESTAMP
                        Extract cases between two timestamps, e.g. --timewindow 2016-07-11T00:00:00Z 2016-07-11T23:59:59Z
  -d or --dry           Dry-Run flag - Do not post to DHIS2, just save import file to logs/notposted/events.json
```

### Cronjob

To install a cronjob which calls the Commcare API for all cases of the last hour (XX:00:00 to XX:59:59) at quarter past every hour:

`crontab -e`
and enter:

`15 * * * * ~/env/bin/python3 ~/commcare-cases-dhis2-events/app/run.py`

## Failures / Log files

The logfile can be found in `commcare-cases-dhis2-events/logs/log.out`

If an `ERROR` occured (it could not post, major errors) it will send out a mail as configured in `config.json`. Upon failure (or _Dry Run mode_), DHIS2-ready import files are stored in `logs/notposted/events-<from>_<to>.json` (but is removed whenever a POST was successful).

## Limitations

- Currently it supports only **100** Commcare cases / hour, but can be expanded.
- It would be possible to send coordinates instead of and orgunit ID. Open an issue for a feature request.
- Concise imports are done if the _Timezones_ of Commcare server **and** DHIS2 server are all UTC.
- Tested with CommCases List Cases API v3+, DHIS2 v2.22 - v2.25
