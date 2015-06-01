# -*- coding: utf-8 -*-
"""
uds.io
~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""


from uds.io.base import IOClient
from uds.io.base import M2MDataDao
from uds.io.console import ConsoleDao
from uds.io.file import FileDao
from uds.io.mysql import MySQLClient
from uds.io.mysql import MySQLDao
from uds.io.evwh import EventWarehouseClient
from uds.io.evwh import EventWarehouseDao


def get_client(store_type, store_params):
    """

    :param store_type:
    :param store_params:
    :return:
    """
    if store_type == 'console':
        return NullClient()

    if store_type == 'file':
        return NullClient()

    if store_type == 'mysql':
        client = MySQLClient(store_params['mysql']['user'],
                             store_params['mysql']['password'],
                             store_params['mysql']['host'],
                             store_params['mysql']['db'])
        return client

    if store_type == 'evwh':
        client = EventWarehouseClient(store_params['evwh']['host'],
                                      store_params['evwh']['port'])
        return client

    if store_type == 'scn':
        return NullClient()

    raise AssertionError('Illegal argument. store_type=' % store_type)


def get_dao(store_type, store_params, sensor_name, start_time, client):
    """
    :param str store_type:
    :param dict store_params:
    :param str table_name:
    :return: dao
    :rtype: M2MDataDao
    """
    if store_type == 'console':
        return ConsoleDao()

    if store_type == 'file':
        return FileDao(sensor_name, start_time, store_params['file']['dir_path'], store_params['file']['dir_file_max'])

    if store_type == 'mysql':
        return MySQLDao(client, store_params['mysql']['table_name'])

    if store_type == 'evwh':
        return EventWarehouseDao(client,
                                 store_params['evwh']['table_name'],
                                 store_params['evwh']['primary_keys_enabled'])

    if store_type == 'scn':
        return NullDao()

    raise AssertionError('Illegal argument. store_type=' % store_type)


class NullClient(IOClient):
    """

    """

    def __init__(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass


class NullDao(M2MDataDao):

    def reconnect(self):
        """Do nothing.

        :return: None
        """
        return None

    def select_last(self, key_data):
        """Do nothing.

        :param key_data:
        :return: None.
        """
        return None

    def insert(self, m2m_data):
        """Do nothing.

        :param m2m_data:
        :return: None.
        """
        return None

