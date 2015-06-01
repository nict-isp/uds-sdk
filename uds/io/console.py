# -*- coding: utf-8 -*-
"""
uds.io.console
~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from uds.io.base import M2MDataDao


class ConsoleDao(M2MDataDao):
    """

    """

    def __init__(self):
        super(ConsoleDao, self).__init__()

    def reconnect(self):
        pass

    def select_last(self, key_data):
        return None

    def insert(self, m2m_data):
        """

        :param m2m_data:
        :return:
        """
        delimiter = '|'

        # View column name
        print '[column]' + delimiter,
        # for device_info
        for key in m2m_data.device_info.keys():
            print str(key) + delimiter,
        # for data_value
        for key in m2m_data.data_values[0].keys():
            print str(key) + delimiter,
        # for unit
        for item in m2m_data.data_schema:
            if 'unit' in item:
                print 'unit_' + str(item['unit']) + delimiter,

        print ''

        # View data
        # for device_info
        for value in m2m_data.device_info.values():
            print str(value) + delimiter,
        print ''

        for idx, datum in enumerate(m2m_data.data_values):
            # for data_value
            for value in datum.values():
                print str(value) + delimiter,
            # for unit
            for item in m2m_data.data_schema:
                if 'unit' in item:
                    print 'unit_' + str(item['unit']) + delimiter,
            print ''
