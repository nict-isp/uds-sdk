# -*- coding: utf-8 -*-
"""
uds.filters
~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import dateutil.parser
import copy
from abc import ABCMeta, abstractmethod

import uds.logging
import uds.io


def get_filter(filter_type, store_type, store_params, sensor_name, start_time):
    if filter_type.lower() == 'no_filter':
        flt = NullFilter()
        return flt

    if filter_type.lower() == 'limited_buffer_filter':
        flt = LimitedBufferedFilter()
        return flt

    if filter_type.lower() == 'time_order_filter':
        client = uds.io.get_client(store_type, store_params)
        client.connect()
        dao = uds.io.get_dao(store_type, store_params, sensor_name, start_time, client)
        finder = LastDataFinder(dao)
        filter_obj = TimeOrderFilter(finder)
        return filter_obj

    raise AssertionError()


class Filter(object):
    """

    """

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def filter(self, m2m_data_list):
        """Delete overlap data in M2M Data list.

        :param m2m_data_list: List of M2M Data.
        :return: Filtered M2M Data list.
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass


class TimeOrderFilter(Filter):
    """TimeOrderFilter delete overlap data in the following way.

    * If new data has not latest time, delete the date.
    * Last data is kept for each primary keys except 'time'.
    * Last data is found from store by LastDataFinder.
    """
    
    def __init__(self, finder):
        super(TimeOrderFilter, self).__init__()
        self._finder = finder

        # Buffer of last data
        self._last_data = {}

    def open(self):
        pass

    def close(self):
        pass

    def filter(self, m2m_data_list):
        """Implementation of super class's method.
        """
        filtered_m2m_data_list = []

        for m2m_data in m2m_data_list:
            filtered_m2m_data = self._filter_one(m2m_data)
            if filtered_m2m_data.size != 0:
                filtered_m2m_data_list.append(filtered_m2m_data)

        # Write log to filtering result.
        before_data_count = 0
        for m2m_data in m2m_data_list:
            before_data_count += m2m_data.size

        after_data_count = 0
        for filtered_m2m_data in filtered_m2m_data_list:
            after_data_count += filtered_m2m_data.size

        uds.logging.info(
            '[filter] before_data_count=%s, after_data_count=%s, memory_last_data_count=%s',
            before_data_count, after_data_count, len(self._last_data)
        )

        return filtered_m2m_data_list
    
    def _filter_one(self, m2m_data):
        """

        :param m2m_data:
        :return: filtered m2m_data
        :rtype: M2MData
        """
        assert 'time' in m2m_data.primary_keys, "Primary keys must include 'time'."
        
        # Prepare result list
        filtered_m2m_data = copy.deepcopy(m2m_data)
        del filtered_m2m_data.data_values[:]

        # Create sorted data order by time
        sorted_tuples = self._to_time_sorted_datum_tuples(m2m_data)

        for tp in sorted_tuples:
            datum = tp[1]
            pk_values = m2m_data.get_pk_values(datum)
            key = self._to_buffer_key(pk_values)
            key_values = self._to_key_values(pk_values)
            
            # Find last data from DAO, and save to buffer.
            if key not in self._last_data:
                str_time = self._finder.find(key_values)
                assert str_time is not False

                self._last_data[key] = dateutil.parser.parse(str_time) if str_time is not None else None
                uds.logging.debug(
                    "[filter] Found last data. location=" + str(key) + ", time=" + str(self._last_data[key]))
            else:
                uds.logging.debug(
                    "[Find Last Data (memory)] location=" + str(key) + ", time=" + str(self._last_data[key]))

            # Check datum whether newest or not.
            sensing_time = tp[0]  # time offset reduced
            last_time = self._last_data[key]
            if last_time is None or last_time < sensing_time:
                filtered_m2m_data.append(datum)
                
                # Update buffer
                self._last_data[key] = sensing_time
            else:
                # print "[Delete Overlap Data]     location=" + str(key) + ", time=" + str(sensorTime)
                pass

        return filtered_m2m_data

    @staticmethod
    def _to_time_sorted_datum_tuples(m2m_data):
        tuples = []
        for datum in m2m_data.data_values:
            # Override time_offset in spatial(legacy) case
            if 'timeOffset' in m2m_data.device_info and m2m_data.device_info['timeOffset'] is not None:
                time_offset = m2m_data.device_info['timeOffset']
            else:
                time_offset = m2m_data.dict['primary']['timezone']

            # Calculate datetime with time offset
            sensing_time = dateutil.parser.parse(datum['time'] + time_offset)

            tp = (sensing_time, datum)
            tuples.append(tp)

        # Sort order by time
        tuples.sort()
        return tuples

    @staticmethod
    def _to_buffer_key(pk_values):
        lst = []
        for pk, v in pk_values.items():
            if pk != 'time':
                lst.append(v)
        tp = tuple(lst)
        return tp

    @staticmethod
    def _to_key_values(pk_values):
        key_values = {}
        for pk, v in pk_values.items():
            if pk != 'time':
                key_values[pk] = v
        return key_values


class LimitedBufferedFilter(Filter):
    """LimitedBufferedFilter delete overlap data in the following way.

    * If new data is duplicated to check buffer, delete the date.
    * Limited number of last data is kept in buffer.
    """

    def __init__(self):
        super(LimitedBufferedFilter, self).__init__()
        self._buffer_size = 1000
        self._buffer_keys = []

    def filter(self, m2m_data_list):
        """Implementation of super class's method.
        """
        filtered_m2m_data_list = []

        for m2m_data in m2m_data_list:
            filtered_m2m_data = self._filter_one(m2m_data)
            if filtered_m2m_data.size != 0:
                filtered_m2m_data_list.append(filtered_m2m_data)

        # Write log to filtering result.
        before_data_count = 0
        for m2m_data in m2m_data_list:
            before_data_count += m2m_data.size

        after_data_count = 0
        for filtered_m2m_data in filtered_m2m_data_list:
            after_data_count += filtered_m2m_data.size

        uds.logging.info(
            '[filter] before_data_count=%s, after_data_count=%s, buffered_data_count=%s',
            before_data_count, after_data_count, len(self._buffer_keys)
        )

        return filtered_m2m_data_list

    def _filter_one(self, m2m_data):
        """

        :param m2m_data:
        :return: filtered m2m_data
        :rtype: M2MData
        """
        # Prepare result list
        filtered_m2m_data = copy.deepcopy(m2m_data)
        del filtered_m2m_data.data_values[:]

        for datum in m2m_data.data_values:
            buffer_key = self._to_buffer_key(m2m_data.get_pk_values(datum))
            if self._is_overlap(buffer_key) is False:
                filtered_m2m_data.append(datum)
            else:
                uds.logging.debug(
                    '[filter] Delete overlap data. buffer_key=%s, data_id=%s', buffer_key, m2m_data.data_id)

        return filtered_m2m_data

    def _is_overlap(self, buffer_key):
        if buffer_key in self._buffer_keys:
            return True
        else:
            if len(self._buffer_keys) >= self._buffer_size:
                self._buffer_keys.pop(0)
            self._buffer_keys.append(buffer_key)
            return False

    @staticmethod
    def _to_buffer_key(pk_values):
        lst = pk_values.values()
        tp = tuple(lst)
        return tp


class NullFilter(Filter):
    """NullFilter do nothing.
    """
    
    def __init__(self):
        super(NullFilter, self).__init__()
    
    def filter(self, m2m_data_list):
        """Do nothing. (Implementation of super class's method.)
        """
        return m2m_data_list


class LastDataFinder(object):
    """LastDataFinder find last data to access destination for storing M2M Data.
    """
    
    def __init__(self, dao):
        self._dao = dao

    def find(self, key_data):
        """Find last data by kay values of data.

        :param key_data:
        :return:
        """
        while True:
            last_datetime = self._find_onetime(key_data)
            if last_datetime is not False:
                return last_datetime

            uds.logging.error('[filter] Failed to find last data. Retry to find...')

    def _find_onetime(self, key_data):
        """
        :return: last_date
        """
        try:
            str_datetime = self._dao.select_last(key_data)
        except Exception as e:
            uds.logging.error(e)

            # Reconnect for next access
            try:
                self._dao.reconnect()
            except Exception as e:
                uds.logging.error(e)

            str_datetime = False
        
        return str_datetime


