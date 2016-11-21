# CommCare Cases to DHIS2 Events

Extract cases from [CommCare](https://www.commcarehq.org/home/) hourly and post them as anonymous events to [DHIS 2](https://www.dhis2.org). Store import failures as JSON files and report errors via mail.

## Installation

- `git clone https://github.com/swisstph/commcare-cases-dhis2-events`
- Install: `cd commcare-cases-dhis2-events` and `$ python setup.py install --user` (this installs it in the user's home directory)
- Run the tests: `python setup.py test` to see if everything is working.
- Note: You may want to use `virtualenv` when using multiple Python projects on this server. ([why?](https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/))

## Configuration

- There are two important files: `config-template.json` which manages credentials and `mapping-template.csv` which manages the mapping of IDs between Commcare and DHIS2. 
- In `config-template.json`, edit the fields (especially `commcare`, `dhis2` and `mail`) and **save** as `config.json`.
- Restrict access to the file: `$ chmod 0600 config.json`
- In CommCare, each case needs a property `userLocationOrgUnitID` which contains the DHIS2 Organisation Unit UID where the Case took place. For other identifiers, check the DHIS2 API docs.

### Mapping file

In `mapping-template.csv`, there are 3 columns:

![mapping.csv](https://i.imgur.com/6XqEVqr.png)

- `commcare_id`: the Commcare case property name. Commcare API: [List Cases (version 3+)](https://confluence.dimagi.com/pages/viewpage.action?pageId=12224287)
- `dhis2_id`: The dataElement UID of DHIS2. DHIS2 API: [Sending events](https://dhis2.github.io/dhis2-docs/master/en/developer/html/webapi_events.html)
- `filter`: Maybe there are Commcare properties that should not be sent to DHIS2, in this case put `EXCLUDE` in this column, `INCLUDE` otherwise. It's best to inspect the CommCare response for this.
- Note that the CSV file must be delimited with `;`

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

`15 * * * * /usr/bin/python ~/commcare-cases-dhis2-events/app/run.py`

## Failures / Log files

The logfile can be found in `commcare-cases-dhis2-events/logs/log.out`

If an `ERROR` occured (it could not post, major errors) it will send out a mail as configured in `config.json`. Upon failure (or _Dry Run mode_), DHIS2-ready import files are stored in `logs/notposted/events-<from>_<to>.json` (but is removed whenever a POST was successful).

## Limitations

- Currently it supports only **100** Commcare cases / hour, but can be expanded.
- It would be possible to send coordinates instead of and orgunit ID. Open an issue for a feature request.
- Python 2.7, no Python 3 support yet
- Concise imports are done if the _Timezones_ of Commcare server **and** DHIS2 server are all UTC.
- Tested with CommCases v3+, DHIS2 v2.22 - v2.25

## Testing

In the working directory, call:
`python -m pytest tests`
or
`python setup.py test`