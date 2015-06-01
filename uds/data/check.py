# -*- coding: utf-8 -*-
"""
uds.data.check
~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import re
import datetime
import dateutil.parser
import pytz

import uds.logging
from uds.data import M2MDataVisitor


class M2MDataChecker(M2MDataVisitor):
    """M2MDataChecker check validity of M2M Data object.
    """

    def __init__(self):
        pass

    def visit_v101(self, m2m_data):
        """Check v1.01 M2M Data.

        :param M2MDataV101 m2m_data: Check target
        :return: If the target is valid, return true, else return False.
        :rtype: :class:`bool`
        """
        device_info = m2m_data.device_info

        # Check info schema
        if 'longitude' not in device_info or device_info['longitude'] is None:
            uds.logging.error('[check] M2M Data schema is invalid. longitude is not in device_info.')
            return False
        if 'latitude' not in device_info or device_info['latitude'] is None:
            uds.logging.error('[check] M2M Data schema is invalid. latitude is not in device_info.')
            return False

        # Check info values
        if self._check_geo_point(m2m_data.device_info['longitude'], m2m_data.device_info['latitude']) is False:
            return False

        for datum in m2m_data.data_values:
            # Check datum schema
            if 'time' not in datum or datum['time'] is None:
                uds.logging.error('[check] M2M Data schema is invalid. time is none.')
                return False

            # Check datum values
            if self._check_time(datum['time'], m2m_data.dict['primary']['timezone']) is False:
                return False

        return True

    def visit_v102(self, m2m_data):
        """Check v1.02 M2M Data.

        :param M2MDataV102 m2m_data: Check target
        :return: If the target is valid, return true, else return False.
        :rtype: :class:`bool`
        """
        # Check info schema
        # => nothing to do

        for datum in m2m_data.data_values:
            # Check datum schema
            if 'time' not in datum or datum['time'] is None:
                uds.logging.error('[check] M2M Data schema is invalid. time is none.')
                return False
            if 'longitude' not in datum or datum['longitude'] is None:
                uds.logging.error('[check] M2M Data schema is invalid. longitude is none.')
                return False
            if 'latitude' not in datum or datum['latitude'] is None:
                uds.logging.error('[check] M2M Data schema is invalid. latitude is none.')
                return False

            # Check datum values
            if self._check_geo_point(datum['longitude'], datum['latitude']) is False:
                return False

            if self._check_time(datum['time'], m2m_data.dict['primary']['timezone']) is False:
                return False

        return True

    @staticmethod
    def _check_geo_point(longitude, latitude):
        # Check whether longitude and latitude is within validity range.
        if longitude < -180 or 180 < longitude or latitude < -90 or 90 < latitude:
            uds.logging.error('[check] Geo point range is invalid. longitude or latitude is out of range.')
            return False
        if longitude == 0 and latitude == 0:
            uds.logging.error('[check] Geo point range is invalid. longitude=latitude=0.')
            return False
        return True

    @staticmethod
    def _check_time(time, offset):
        if offset is None:
            uds.logging.error('[check] timezone is none.')
            return False

        # Check whether sensor time is earlier than current time.
        try:
            sensor_time = dateutil.parser.parse(time+offset)          # sensor time
            now_time = pytz.utc.localize(datetime.datetime.utcnow())  # current time
        except Exception as e:
            uds.logging.error(
                '[check] time or timezone format is invalid. time={0}, timezone={1}, parse_error={2}'.format(
                    str(time), str(offset), str(e)))
            return False

        # 10分以上未来の場合、エラーとする
        if (now_time - sensor_time) > datetime.timedelta(minutes=-10):
            return True
        else:
            uds.logging.error('[check] Sensing time is out of range.')
            return False




