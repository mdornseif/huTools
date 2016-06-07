#!/usr/bin/env python
# encoding: utf-8
"""
formats.py - formating and parsing of timestamps.

Created by Maximillian Dornseif on 2007-06-24.
Copyright (c) 2007, 2010 HUDORA GmbH. All rights reserved.
"""

import unittest
import datetime
import decimal
import doctest
import time
import email.utils


def german_weekday_name(date):
    """Return the german weekday name for a given date."""
    days = [u'Montag', u'Dienstag', u'Mittwoch', u'Donnerstag', u'Freitag', u'Samstag', u'Sonntag']
    return days[date.weekday()]


def german_month_name(date):
    """Return the german month name for a given date."""
    months = [u'Januar', u'Februar', u'März', u'April', u'Mai', u'Juni', u'Juli', u'August',
              u'September', u'Oktober', u'November', u'Dezember']
    return months[date.month - 1]


def tertial(date):
    """Wandelt ein Date oder Datetime-Objekt in einen Tertial-String"""
    ret = date.strftime('%Y-%m')
    ret = ret[:-2] + {'01': 'A', '02': 'A', '03': 'A', '04': 'A',
                      '05': 'B', '06': 'B', '07': 'B', '08': 'B',
                      '09': 'C', '10': 'C', '11': 'C', '12': 'C'}[ret[-2:]]
    return ret


def rfc3339_date(date=None):
    """Formates a datetime object according to RfC 3339."""
    date = date or datetime.datetime.now()
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def rfc3339_date_parse(date):
    """Parses an RfC 3339 timestamp into a datetime object."""
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')


def convert_to_date(date):
    """Converts argument into a date object.

    Assumes argument to be a RfC 3339 coded date or a date(time) object.
    """

    if isinstance(date, datetime.datetime):
        return date.date()
    elif isinstance(date, datetime.date):
        return date
    elif not date:
        return None
    elif isinstance(date, basestring):
        date = date[:10]  # strip time
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            try:
                date = date[:8]  # strip time
                return datetime.datetime.strptime(date, '%Y%m%d').date()
            except ValueError:
                pass  # Error will be raised later on
    raise ValueError("Unknown date value %r (%s)" % (date, type(date)))


def fraction_to_microseconds(fraction):
    """
    Convert the fractional part to microseconds

    >>> fraction_to_microseconds('1')
    100000
    >>> fraction_to_microseconds(12)
    120000
    >>> fraction_to_microseconds(123)
    123000
    >>> fraction_to_microseconds('1234')
    123400
    >>> fraction_to_microseconds('12345')
    123450
    >>> fraction_to_microseconds('123456')
    123456
    >>> fraction_to_microseconds('1234567')
    123456
    """
    if isinstance(fraction, (int, long)):
        fraction = str(fraction)
    return int(decimal.Decimal('0.' + fraction) * 1000000)


def _parse_timestamp(timestamp):
    """Try to parse timestamp with various formats"""

    for fmt in '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y%m%dT%H%M%S':
        try:
            return datetime.datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise


def convert_to_datetime(date):
    """Converts argument into a datetime object.

    Assumes argument to be a RfC 3339 coded date or a date(time) object.
    """

    if isinstance(date, datetime.datetime):
        return date
    elif isinstance(date, datetime.date):  # order mattes! datetime is a subclass of date
        return datetime.datetime.combine(date, datetime.time())
    elif isinstance(date, basestring):
        if len(date) < 11:
            return convert_to_datetime(convert_to_date(date))
        else:
            # remove Timezone
            if date.endswith(' +0000'):
                date = date.rstrip(' +0')
            date = date.rstrip('Z')

            # handle milliseconds
            ms = 0
            if '.' in date:
                date, ms = date.split('.')

            # Might need to append seconds
            if 1 < len(date.split(':')) < 3:
                date = date + ':00'

            ret = _parse_timestamp(date)
            if ms:
                ret = ret.replace(microsecond=fraction_to_microseconds(ms))
            return ret
    elif not date:
        return None
    raise ValueError("Unknown value %r (%s)" % (date, type(date)))


def rfc2616_date(date=None):
    """Formates a datetime object according to RfC 2616.

    RfC 2616 is a subset of RFC 1123 date.
    Weekday and month names for HTTP date/time formatting; always English!
    """
    if date is None:
        date = datetime.datetime.now()
    return email.utils.formatdate(time.mktime(date.timetuple()), usegmt=True)


def rfc2616_date_parse(data):
    """Parses an RfC 2616/2822 timestapm into a datetime object."""
    return datetime.datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(data)))


class _FormatsTests(unittest.TestCase):

    def test_rfc3339_date(self):
        """Test basic rfc3339_date output."""
        self.assertEqual(rfc3339_date(datetime.datetime(2007, 2, 3, 4, 5, 6)), '2007-02-03T04:05:06Z')

    def test_rfc3339_date_parse(self):
        """Test basic rfc3339_date_parse output."""
        self.assertEqual(rfc3339_date_parse('2007-02-03T04:05:06Z'),
                         datetime.datetime(2007, 2, 3, 4, 5, 6))

    def test_rfc2616_date(self):
        """Test basic rfc2616_date output."""
        self.assertEqual(rfc2616_date(datetime.datetime(2007, 2, 3, 4, 5, 6)),
                         'Sat, 03 Feb 2007 03:05:06 GMT')

    def test_rfc2616_date_parse(self):
        """Test basic rfc2616_date_parse output."""
        self.assertEqual(rfc2616_date_parse('Sat, 03 Feb 2007 03:05:06 GMT'),
                         datetime.datetime(2007, 2, 3, 4, 5, 6))

    def test_convert_to_datetime(self):
        """Test convert_to_datetime() and convert_to_date() functionality"""
        self.assertEqual(convert_to_datetime(datetime.date(2007, 2, 3)),
                         datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime(datetime.datetime(2007, 2, 3, 13, 14, 15, 16)),
                         datetime.datetime(2007, 2, 3, 13, 14, 15, 16))
        self.assertEqual(convert_to_datetime('2007-02-03'), datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime('2007-2-3'), datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime('20070203'), datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime('20070203T131415'), datetime.datetime(2007, 2, 3, 13, 14, 15))
        self.assertEqual(convert_to_datetime('2007-02-03T13:14:15'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15))
        self.assertEqual(convert_to_datetime('2007-02-03T13:14:15.16'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15, 160000))
        self.assertEqual(convert_to_datetime('2007-02-03 13:14:15'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15))
        self.assertEqual(convert_to_datetime('2007-02-03 13:14:15.16'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15, 160000))
        self.assertEqual(convert_to_datetime('2013-09-03 21:39:09 +0000'),
                         datetime.datetime(2013, 9, 3, 21, 39, 9))
        self.assertEqual(convert_to_datetime('2013-12-03 13:14'),
                         datetime.datetime(2013, 12, 3, 13, 14, 0, 0))

        self.assertEqual(convert_to_datetime('2013-12-03 13:14:05.23'),
                         datetime.datetime(2013, 12, 3, 13, 14, 5, 230000))
        timestamp = convert_to_datetime('2013-12-03 13:14:05.23')
        self.assertEqual(timestamp.isoformat(), '2013-12-03T13:14:05.230000')
        timestamp = convert_to_datetime('2013-12-03T13:14:05.2')
        self.assertEqual(timestamp.isoformat().rstrip('0'), '2013-12-03T13:14:05.2')


class _ApiTests(unittest.TestCase):

    def test_defaults(self):
        """Test rfc3339_date defaults"""
        rfc3339_date()
        rfc2616_date()


if __name__ == '__main__':
    doctest.testmod()
    unittest.main()
