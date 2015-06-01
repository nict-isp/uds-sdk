# -*- coding: utf-8 -*-
"""
uds.contrib.io.evwh
~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import socket
import struct
import datetime
import select
import json

import uds.logging
from uds.io.base import M2MDataDao


class EventWarehouseDao(M2MDataDao):
    """
    """

    def __init__(self, client, table_name, primary_keys_enabled=False):
        self._client = client
        self._table_name = table_name
        self._column = 'observation'
        self._primary_keys_enabled = primary_keys_enabled

    def reconnect(self):
        self._client.disconnect()
        self._client.connect()

    def select_last(self, key_values):
        # Execute query
        query = self._create_select_query(key_values)
        str_response = self._client.send(query)

        # Handle response
        dict_response = json.loads(str_response)
        if 'events' in dict_response:
            # Success case
            events = dict_response['events']
            if len(events) > 0:
                str_time = events[0]['observation']['when']['time']
            else:
                str_time = None
            return str_time
        else:
            # Error case
            uds.logging.error('[io.evwh] EvWH returns error. response=%s', dict_response)
            return False

    def insert(self, m2m_data):
        # Execute query
        query = self._create_insert_query(m2m_data)
        str_response = self._client.send(query)

        # Handle response
        dict_response = json.loads(str_response)
        if 'result' in dict_response and dict_response['result'] is True:
            # Success case:
            uds.logging.info("[io.evwh] Succeed in storing.")
            uds.logging.info("[io.evwh] > response=%s", str_response)
            uds.logging.info("[io.evwh] > query=%s", _get_limit_string(query, 50))
            return True
        else:
            # Error case:
            # Write error message to log
            if 'error' in dict_response:
                error_message = dict_response['error']
                uds.logging.error("[io.evwh] EvWH returns error result.")
                uds.logging.error("[io.evwh] > error_message=%s", error_message)
                uds.logging.error("[io.evwh] > query=%s", query)
            else:
                uds.logging.error("[io.evwh] EvtWH returns error result. Failed to parse error_message.")
                uds.logging.error("[io.evwh] > query=%s", query)

            return False

    def _create_select_query(self, key_values):
        """Create SELECT statement of MPQL for last data.
        Example:
            SELECT(0) observation FROM JMA1hRainFall
            WHERE COMPARE(observation, POINT(137.1289712 35.3325027),'=')
            ORDER BY observation TIME DESC
            LIMIT 5

        :return: statement
        :rtype: str
        """
        # Create WHERE statement
        compares = []

        if 'latitude' in key_values and 'longitude' in key_values:
            longitude = _get_mpql_quoted_string(key_values['longitude'])
            latitude = _get_mpql_quoted_string(key_values['latitude'])
            compare = "COMPARE(observation, POINT({longitude} {latitude}),'=')".format(
                longitude=longitude, latitude=latitude)
            compares.append(compare)

        for k, v in key_values.items():
            if k not in ['time', 'latitude', 'longitude']:
                compare = "COMPARE(observation, THEME({theme_name}, '{value}'),'=')".format(
                    theme_name=k, value=_get_mpql_quoted_string(v))
                compares.append(compare)

        if len(compares) > 0:
            stmt_where = "WHERE " + " AND ".join(compares)
        else:
            stmt_where = ""

        # Create other conditions
        stmt_others = "ORDER BY observation TIME DESC LIMIT 5"

        # Create query
        result = "SELECT(0) {column} FROM {table} {stmt_where} {stmt_others}".format(
            column=self._column,
            table=self._table_name,
            stmt_where=stmt_where,
            stmt_others=stmt_others
        )
        return result

    def _create_insert_query(self, m2m_data):
        """Create INSERT statement of MPQL.
        Query Example::

            INSERT INTO
                table_name(column_name) VALUES(M2M("M2M Format Data"))
            WHERE
                COMPARE(observation,TIMESTAMP("2012-03-12T12:34:59.999+0000"),"=") AND
                COMPARE(observation,POINT(56.0 -13.2),"=")

        :param m2m_data:
        :return: INSERT statement
        :rtype: str
        """
        # Create stmt_values
        stmt_values = "VALUES( M2M(\"" + m2m_data.json.replace('"', '""').replace("'", "''") + "\"))"

        # Get primary keys with datum value
        if not self._primary_keys_enabled:
            pk_values = {}
        elif m2m_data.size == 1:
            pk_values = m2m_data.get_pk_values(m2m_data[0])
        else:
            raise Exception(
                "Unsupported M2MData object for Conditional Insert of Event Warehouse."
                "The M2MData object has data collection in data section."
            )

        # Create conditions of stmt_where
        conditions = []

        if 'latitude' in pk_values and 'longitude' in pk_values and 'time' in pk_values:
            condition = 'SPATIOTEMPORAL({column})'.format(column=self._column)
            conditions.append(condition)

        for k, v in pk_values.items():
            if k not in ['latitude', 'longitude', 'time']:
                condition = "COMPARE(observation, THEME({theme_name}, {value}),'=')".format(
                    theme_name=k, value=_get_mpql_quoted_string(v))
                conditions.append(condition)

        # Create statement
        if len(conditions) > 0:
            stmt_where = "WHERE " + " AND ".join(conditions)
            result = "INSERT INTO {table}({column}) {stmt_values} {stmt_where}".format(
                table=self._table_name, column=self._column, stmt_values=stmt_values, stmt_where=stmt_where)
        else:
            result = "INSERT INTO {table}({column}) {stmt_values}".format(
                table=self._table_name, column=self._column, stmt_values=stmt_values)

        return result


class EventWarehouseClient(object):
    """

    """

    def __init__(self, host, port):
        super(EventWarehouseClient, self).__init__()
        self._table_hash = {}

        self._timeout = 2
        self._host = host
        self._port = int(port)
        self._sock = None

    @property
    def timeout(self):
        """ Timeout period(second). Default value is 2 second.
        :getter:
        :setter:
        :type: int
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def connect(self):
        """Connect to Event Warehouse.

        :return: None
        """
        try:
            self._sock = socket.socket()
            self._sock.connect((self._host, self._port))
        except Exception as e:
            uds.logging.error('[io.evwh] Failed to connect EvWH. error=%s', e)

    def disconnect(self):
        """ Disconnect.

        :return: None.
        """
        self._sock.close()

    def send(self, query):
        """Send query to Event Warehouse.

        :param query: MPQL query.
        :return: response
        :rtype: JSON string.
        """
        seq = 10001
        self._sock.sendall(data_to_byte(seq, query))
        container = MessageContainer()

        while True:
            ready_to_read, ready_to_write, in_error = select.select([self._sock], [], [self._sock], self._timeout)
            if len(in_error) > 0 and in_error[0] == self._sock:
                uds.logging.error('[io.evwh] ' + string_now() + ',' + str(seq) + ',error')
                return False

            elif len(ready_to_read) > 0 and ready_to_read[0] == self._sock:
                recv = self._sock.recv(1024)
                if len(recv) > 0:
                    container.add(recv)
                    if container.complete():
                        # Print response for debug
                        # print(string_now() + ',' + str(container.get_seq()) + ',end')
                        # print("return = " + str(container.get_json()) + ", query = " + query)
                        # print(string_now() + ',' + str(container.get_seq()) + ',size,' + str(container.get_size()+8))
                        break
                else:
                    container.clear()
                    uds.logging.error('[io.evwh] Event Warehouse time out.')
                    return False
            elif len(ready_to_write) > 0:
                continue  # ignore

            elif len(ready_to_write) == 0:
                container.clear()
                uds.logging.error('[io.evwh] Event Warehouse time out.')
                return False

        return container.get_json()


class MessageContainer:
    def __init__(self):
        self.recv = None
        self.size = None
        self.seq = None
        self.json = None

    def add(self, recv):
        if self.recv is None:
            self.recv = recv
            self.size = len(recv)
        else:
            self.recv += recv
            self.size += len(recv)

    def get_size(self):
        return self.size

    def get_seq(self):
        return self.seq

    def get_json(self):
        return self.json

    def clear(self):
        self.recv = None
        self.size = None

    def complete(self):
        if len(self.recv) >= 8:
            self.size, self.seq = struct.Struct('>II').unpack_from(self.recv)
            if len(self.recv) >= self.size + 8:
                self.json = str(struct.Struct('>' + str(self.size) + 's').unpack_from(self.recv, 8)[0])
                return True
        return False


def data_to_byte(seq, mpql):
    size = len(mpql.encode())
    values = (size, seq, mpql.encode())
    s = struct.Struct(">II" + str(size) + "s")
    return s.pack(*values)


def string_now():
    return str(datetime.datetime.today())


def try_create_table(client, table_name):
    """Check for the table existence, and if not exist, create the table.

    :param client:
    :param table_name:
    :return: None or response.
    """
    if check_table(client, table_name):
        pass
    else:
        create_table(client, table_name)


def check_table(client, table_name):
    """Check for the table existence.

    :param client:
    :param table_name: table name.
    :return: if exist, return True, else return False.
    """
    if table_name is None or table_name == '':
        raise AssertionError()

    table_hash = json.loads(get_tables(client))

    if table_hash.has_key('tables') and table_hash['tables'].has_key(table_name):
        return True
    else:
        return False


def get_tables(client):
    """Get table list in Event Warehouse.

    :param client:
    :return: response
    """
    return client.send("SELECT GetTables")


def create_table(client, table_name):
    """Create table.

    :param client:
    :param table_name:
    :return: response
    """
    query = "CREATE TABLE {table_name} (observation EVENT)".format(table_name=table_name)
    return client.send(query)


def _get_mpql_quoted_string(value):
    if isinstance(value, int):
        return repr(value)
    elif isinstance(value, float):
        return repr(value)
    elif isinstance(value, str):
        return "'" + value + "'"
    elif isinstance(value, unicode):
        return "'" + value + "'"
    else:
        raise Exception("Unexpected type of value for MPQL statement.")


def _get_limit_string(value, limit):
    if len(value) > limit:
        return value[0:limit] + "..."
    else:
        return value