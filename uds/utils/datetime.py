# -*- coding: utf-8 -*-
"""
uds.utils.datetime
~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from __future__ import absolute_import

import re
import datetime
import dateutil.parser
import pytz


def normalize_timezone(timezone):
    """

    :param time_zone:
    :return: normalized value
    """
    try:
        # Check
        dateutil.parser.parse('2013/1/1 00:00' + timezone)
        return timezone
    except:
        # Normalize
        result = re.search('([\+-][0-9][0-9]:[0-9][0-9])', timezone).group(0)
        # Recheck
        dateutil.parser.parse('2013/1/1 00:00' + result)
        return result


def get_now_time(timezone):
    """Returns current datetime adjusted to timezone.

    :param timezone:
    :return: current date time
    :rtype: :class:`str`
    """
    # '2013/1/1 00:00' with timezone
    try:
        tmpTimeOn = dateutil.parser.parse('2013/1/1 00:00' + timezone)
    except:
        timezone = re.search('([\+-][0-9][0-9]:[0-9][0-9])', timezone).group(0)
        tmpTimeOn = dateutil.parser.parse('2013/1/1 00:00' + timezone)
        
    # '2013/1/1 00:00' as UTC
    tmpTimeOff = dateutil.parser.parse('2013/1/1 00:00+00:00')

    # Get time offset
    timeOffset = tmpTimeOn - tmpTimeOff

    # Get current time as UTC
    utcNow = pytz.utc.localize(datetime.datetime.utcnow())

    # Adjust timezone
    tzoneNow = utcNow - timeOffset
    tzoneNow = tzoneNow.replace(tzinfo=None)
    
    return str(tzoneNow)