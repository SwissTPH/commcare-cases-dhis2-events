#!/usr/bin/env python
#
# Copyright 2001-2002 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# This file is part of the Python logging distribution. See
# http://www.red-dove.com/python_logging.html
#
"""Test harness for the logging module. Tests BufferingSMTPHandler, an
alternative implementation SMTPHandler.
This fork includes credential and secure support (as implemented in
newer versions of logging library). Additionaly a flood check is
implemented to make sure not more than capacity per minute is sent,
otherwise the capacity (buffer) is raised to the power of 2.
Copyright (C) 2001-2002 Vinay Sajip. All Rights Reserved.
Copyright (C) 2013 Pavel Savchenko. All Rights Reserved.
"""
import logging
import logging.handlers
import string
import time


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, capacity,
                 credentials=None, secure=None):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.start_counting = time.time()
        self.counter = 0
        self.mailhost = mailhost
        self.mailport = 587
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.secure = secure

        if isinstance(credentials, tuple):
            self.username, self.password = credentials
        else:
            self.username = None

        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-s %(message)s"))

    def flush(self):
        if self.counter > self.capacity:
            self.capacity = self.capacity * self.capacity  # raise buffer capacity
        else:
            self.capacity = self.capacity  # lower buffer capacity back

        if time.time() - self.start_counting > 60:
            self.start_counting = time.time()
            self.counter = 0

        if len(self.buffer) > 0:
            try:
                import smtplib
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n".format(self.fromaddr, ",".join(self.toaddrs), self.subject)
                for record in self.buffer:
                    s = self.format(record)
                    print(s)
                    msg = msg + s + "\r\n"
                    self.counter += 1
                if self.username:
                    if self.secure is not None:
                        smtp.ehlo()
                        smtp.starttls(*self.secure)
                        smtp.ehlo()
                    smtp.login(self.username, self.password)
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []
