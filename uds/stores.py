# -*- coding: utf-8 -*-
"""
uds.stores
~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from abc import ABCMeta, abstractmethod

import uds.logging
from uds.io.console import ConsoleDao
from uds.io.file import FileDao
from uds.io import mysql
from uds.io.mysql import MySQLClient
from uds.io.mysql import MySQLDao
from uds.io import evwh
from uds.io.evwh import EventWarehouseClient
from uds.io.evwh import EventWarehouseDao


def get_store(store_type, store_params, sensor_name, start_time):
    if store_type.lower() == 'console':
        return ConsoleStore()

    elif store_type.lower() == 'file':
        return FileStore(store_params['file'], sensor_name, start_time)

    elif store_type.lower() == 'mysql':
        return MySQLStore(store_params['mysql'], sensor_name)

    elif store_type.lower() == 'evwh':
        return EventWarehouseStore(store_params['evwh'], store_params['file'], sensor_name, start_time)

    elif store_type.lower() == 'scn':
        return SCNStore(store_params['scn'], sensor_name)

    else:
        try:
            import uds.contrib.stores
            return uds.contrib.stores.get_store(store_type, store_params, sensor_name, start_time)
        except ImportError:
            pass

    raise AssertionError('Illegal argument. store_type=' % store_type)


class Store(object):
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
    def store(self, m2m_data_list):
        """Store M2M Data to selected destination.

        :param m2m_data_list: List of M2M Data
        :return: None
        """
        pass


class ConsoleStore(Store):
    """ConsoleStore redirect M2MData list to console.
    This class is used for debug.
    """

    def __init__(self):
        super(ConsoleStore, self).__init__()
        self._dao = ConsoleDao()

    def store(self, m2m_data_list):
        """Implementation of super class's method.
        """
        for m2m_data in m2m_data_list:
            self._dao.insert(m2m_data)


class FileStore(Store):
    """FileStore store M2M Data to local file.

    Directory structure::

        * m2m_data
            -   [title][start-up datetime]/
                -   0000000000/
                    -   M2MmetaData[title][creation datetime].json
                    -   M2MData[title][creation datetime].json

    Example of directory::

        * m2_mdata/
            -   JapanRaditionSensor20130926144347/
                -   0000000000/
                    -   M2MmetaDataExampleSensor20130926144352129000.json
                    -   M2MDataExampleSensor20130926144352129000.json
    """

    def __init__(self, file_params, sensor_name, start_time):
        super(FileStore, self).__init__()
        self._file_params = file_params
        self._sensor_name = sensor_name
        self._start_time = start_time
        self._dao = None

    def open(self):
        dir_path = self._file_params['dir_path']

        self._dao = FileDao(self._sensor_name, self._start_time, dir_path, self._file_params['dir_file_max'])

    def store(self, m2m_data_list):
        """Implementation of super class's method.
        """
        for m2m_data in m2m_data_list:
            # Write message to log.
            uds.logging.info("[store] Store m2m_data to file. data_id=%s, latitude=%s, longitude=%s, time=%s",
                             m2m_data.data_id,
                             repr(m2m_data.north),
                             repr(m2m_data.south),
                             str(m2m_data.min_time))

            self._dao.insert(m2m_data)


class MySQLStore(Store):
    """MySQLStore store M2M Data to MySQL Database.

    *   You need to prepare MySQL database to store.
    *   MySQLStore automatically create new table for output data.
    """

    def __init__(self, mysql_params, sensor_name):
        super(MySQLStore, self).__init__()
        self._mysql_params = mysql_params
        self._client = None
        self._dao = None
        self._is_first_data = True

    def open(self):
        super(MySQLStore, self).open()

        # Setup connection to MySQL
        self._client = MySQLClient(self._mysql_params['user'],
                                   self._mysql_params['password'],
                                   self._mysql_params['host'],
                                   self._mysql_params['db'])
        # Setup DAO
        self._dao = MySQLDao(self._client, self._mysql_params['table_name'])

    def store(self, m2m_data_list):
        """Implementation of super class's method.
        """
        self._client.connect()

        # Check and create table
        if self._is_first_data:
            mysql.try_create_m2m_table(self._client, self._mysql_params['table_name'], m2m_data_list[0])
            self._is_first_data = False

        for m2m_data in m2m_data_list:

            # Write message to log.
            uds.logging.info("[store] Store m2m_data to MySQL. data_id=%s, latitude=%s, longitude=%s, time=%s",
                             m2m_data.data_id,
                             repr(m2m_data.north),
                             repr(m2m_data.south),
                             str(m2m_data.min_time))

            self._dao.insert(m2m_data)

        self._client.disconnect()


class EventWarehouseStore(Store):
    """

    """

    def __init__(self, evwh_params, file_params, sensor_name, start_time):
        super(EventWarehouseStore, self).__init__()
        self._evwh_params = evwh_params
        self._file_params = file_params
        self._sensor_name = sensor_name
        self._start_time = start_time
        self._client = None
        self._evwh_dao = None
        self._file_dao = None

    def open(self):
        super(EventWarehouseStore, self).open()

        # Setup connection to Event Warehouse
        self._client = EventWarehouseClient(self._evwh_params['host'], self._evwh_params['port'])
        self._client.connect()

        # Check and create table
        evwh.try_create_table(self._client, self._evwh_params['table_name'])

        # Set insert_timeout
        self._client.timeout = self._evwh_params['insert_timeout']

        # Setup EventWarehouseDao
        self._evwh_dao = EventWarehouseDao(
            self._client, self._evwh_params['table_name'], self._evwh_params['primary_keys_enabled'])

        # Setup FileDao for Event Warehouse ERROR
        self._file_dao = FileDao(self._sensor_name,
                                 self._start_time,
                                 self._evwh_params['error_dir_path'],
                                 self._file_params['dir_file_max'])

    def store(self, m2m_data_list):
        """Store m2m_data_list to Event Warehouse.
        If fail to store, store data to local file.
        """
        send_count = 0
        send_failed_count = 0

        for m2m_data in m2m_data_list:

            # Write message to log.
            uds.logging.info("[store] Store m2m_data to EvWH. data_id={0}, latitude={1}, longitude={2}, time={3}".format(
                str(m2m_data.data_id), repr(m2m_data.north), repr(m2m_data.south), str(m2m_data.min_time)))

            # Execute insert
            send_count += 1
            try:
                is_success = self._evwh_dao.insert(m2m_data)
            except Exception as e:
                uds.logging.critical(
                    '[store] Unexpected error occurred during execute insert query to EvWH. e={0}' + str(e))
                is_success = False

            if is_success is False:
                # When error, store to file.
                self._file_dao.insert(m2m_data)
                send_failed_count += 1

                # Reconnect to EvWH for next insert.
                try:
                    self._evwh_dao.reconnect()
                except Exception as e:
                    uds.logging.critical(
                        '[store] Exception occurred during connect to EvWH. e={0}' + str(e))


class SCNStore(Store):
    """

    """

    def __init__(self, scn_params, sensor_name):
        super(SCNStore, self).__init__()
        self._scn_params = scn_params
        self._sensor_name = sensor_name
        self._scn = None

    def open(self):
        super(SCNStore, self).open()

        self._scn = SCNApi(
            self._sensor_name,
            self._scn_params['service_info'],
            self._scn_params['module_path'],
            self._scn_params['stub_module_enabled']
        )

        # Register sensor service to SCN.
        self._scn.create_service()

    def store(self, m2m_data_list):
        """Store m2m_data_list to Event Warehouse.
        """

        for m2m_data in m2m_data_list:

            # Write message to log.
            uds.logging.info("[store] Store m2m_data to SCN. data_id={0}, latitude={1}, longitude={2}, time={3}".format(
                str(m2m_data.data_id), repr(m2m_data.north), repr(m2m_data.south), str(m2m_data.min_time)))

            # FIXME: Check deprecated send format!
            # scn_m2m_dict = {'MetaData': m2m_data.metadata_dict, 'Data': m2m_data.data_dict}
            # scn_m2m_json = json.dumps(scn_m2m_dict)

            # Send data to SCN
            self._scn.send_data(m2m_data.json)
