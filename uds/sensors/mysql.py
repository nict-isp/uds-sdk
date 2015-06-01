# -*- coding: utf-8 -*-
"""
uds.sensors.mysql
~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from abc import abstractmethod

import uds.logging
from uds.sensors.base import Sensor
from uds.utils.crawling import Pacemaker
from uds.io.mysql import MySQLClient


class MySQLSensor(Sensor):
    """

    """

    def __init__(self, project_home):
        super(MySQLSensor, self).__init__(project_home)
        self._interval = 0
        self._mysql_fetch_params = {
            'user': None,
            'password': None,
            'host': None,
            'db': None,
        }

        self._pacemaker = None
        self._fetch_client = None

    @property
    def interval(self):
        """Second-scale interval of fetching data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: int
        """
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def mysql_fetch_params(self):
        """Information of MySQL connection for fetching rows.

        Example usage:

        ::

            self.mysql_fetch_params = {
                'user': your_name,
                'password': abc123,
                'host': 192.168.1.1,
                'db': MyDatabase,
            }

        :getter: Returns this parameter
        :type: dict
        """
        return self._mysql_fetch_params

    @mysql_fetch_params.setter
    def mysql_fetch_params(self, values):
        self._mysql_fetch_params = values
        
    def open(self):
        """Override of super class's method.
        """
        super(MySQLSensor, self).open()
        self._pacemaker = Pacemaker(self.interval)
        self._fetch_client = MySQLClient(
            self._mysql_fetch_params['user'],
            self._mysql_fetch_params['password'],
            self._mysql_fetch_params['host'],
            self._mysql_fetch_params['db']
        )

    def fetch(self):
        """Fetch rows from MySQL table.

        :return: Result rows
        :rtype: list
        """
        self._pacemaker.wait()
        query = self.create_query()
        
        if query is None:
            uds.logging.error('[fetch] ' + __class__ + ' It is necessary for you to do call')
            return False
        
        # Connect to MySQL
        self._fetch_client.connect()
        
        # Execute select query
        rows = self._fetch_client.send(query)

        # Disconnect MySQL
        self._fetch_client.disconnect()
        
        return rows

    @abstractmethod
    def create_query(self):
        """Create query to fetch rows.

        :return: SQL SELECT statement
        :rtype: str
        """
        pass

    def parse(self, source):
        """Override of super class's method.
        """
        return self.parse_rows(source)

    @abstractmethod
    def parse_rows(self, rows):
        """Parse result rows to list of M2M Data.

        :param rows: result rows
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass
        
        

