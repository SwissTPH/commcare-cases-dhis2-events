#!/usr/bin/env python

import logging
import logging.handlers
import os
import sys

try:
    from mail import BufferingSMTPHandler
except ImportError:
    from app.helpers.mail import BufferingSMTPHandler

logger = logging.getLogger('__name__')


def init_logger(config):
    """ initialize logging utility, including sending errors as mail"""
    # do not change the level here
    logger.setLevel(logging.DEBUG)

    # only log requests and urllib3 warning messages
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.ERROR)

    path = os.path.abspath(os.path.dirname(__file__))[:-11]
    # set up filelogger with maximum log file size and no. of backup files
    file_log_path = os.path.join(path, "logs", "log.out")
    rotating_file_log = logging.handlers.RotatingFileHandler(file_log_path, maxBytes=3 * 1048576, backupCount=20)
    rotating_file_log.setLevel(eval(config['log']['fileloglevel']))

    # set up mailsender for logs
    MAILHOST = config['mail']['host']
    FROM = config['mail']['from']
    TO = config['mail']['to']
    SUBJECT = config['mail']['subject']
    MAILUSERNAME = config['mail']['username']
    MAILPASSWORD = config['mail']['password']

    mail_file_log = BufferingSMTPHandler(MAILHOST, FROM, TO, SUBJECT, 10,
                                         credentials=(MAILUSERNAME, MAILPASSWORD), secure=())
    mail_file_log.setLevel(eval(config['log']['mailloglevel']))

    # set up format for log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    rotating_file_log.setFormatter(formatter)
    mail_file_log.setFormatter(formatter)

    # add both loggers to the root logger
    logger.addHandler(rotating_file_log)
    logger.addHandler(mail_file_log)


def log_debug(text):
    logger.debug(text)


def log_info(text):
    logger.info(text)
    print(text)


def log_error(text):
    logger.error(text)
    print(text)
    sys.exit()
