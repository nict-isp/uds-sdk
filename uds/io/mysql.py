# -*- coding: utf-8 -*-
"""
uds.is.mysql
~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import MySQLdb

import uds.logging
from uds.io.base import M2MDataDao


class MySQLDao(M2MDataDao):
    """
    """

    def __init__(self, client, table_name):
        super(MySQLDao, self).__init__()

        self._client = client
        self._table_name = table_name

    def reconnect(self):
        self._client.disconnect()
        self._client.connect()

    def select_last(self, key_data):
        pass

    def insert(self, m2m_data):

        columns = []  # Column Names
        values = []   # Datum Values

        for datum in m2m_data.data_values:

            for key, value in datum.items():
                if value is not None:
                    columns.append(key)
                    values.append(value)

            for key, value in m2m_data.device_info.items():
                if value is not None:
                    columns.append(key)
                    values.append(value)

            for key, value in m2m_data.data_units.items():
                if key in ['time', 'longitude', 'latitude']:
                    continue
                if value is not None:
                    columns.append('unit_' + key)
                    values.append(value)

            for key, value in m2m_data.info_summary.items():
                if value is not None:
                    columns.append(key)
                    values.append(value)

            if 'timezone' in columns:
                pass
            else:
                columns.append('timezone')
                values.append(m2m_data.dict['primary']['timezone'])

        self.insert_values(columns, values)

        self._client.commit()

    def insert_json(self, hash):
        """Insert JSON data.
        """
        t_str = "INSERT INTO " + self._table_name

        info_str = "( "
        value_str = "VALUES ( "

        for info, value in hash.iteritems():
            info_str += info
            info_str += ", "
            value_str += ("\'" + value + "\'")
            value_str += ", "

        info_str = info_str.rstrip(", ")
        value_str = value_str.rstrip(", ")

        info_str += ")"
        value_str += ")"

        t_str = t_str + info_str + value_str

        res = None
        try:
            # print "debug: ", t_str
            self._client.send(t_str)
            insert_id = self._client.insert_id()
            res = self._client.commit()
            if res is None:
                res = insert_id
        except Exception, e:
            print "DB Insert Fail: {0} {1}".format(e, t_str)

        return res

    def insert_values(self, columns, values):
        # print values
        com_header = "INSERT  INTO"
        t_str = com_header + " " + self._table_name + "("
        for id in range(0, len(columns)):
            if id < (len(columns) - 1):
                t_str += "`" + columns[id] + "`, "
            else:
                t_str += "`" + columns[id] + "`) "

        t_str += "values ("

        for id in range(0, len(values)):

            if columns[id] != 'timezone' and _type_to_string(values[id]) == 'float':
                t_str += str(values[id]).replace("'", "\\'")
            else:
                values[id] = str(values[id]).replace("'", "\\'")
                if values[id].find("Point") >= 0 or values[id].find("Polygon") >= 0:
                    values[id] = "GeomFromText(\'" + values[id] + "\')"
                    # print values[id]
                    t_str += values[id]
                else:
                    t_str += "'" + values[id] + "'"

            if id < (len(values) - 1):
                t_str += ", "
            else:
                t_str += "); "

                # print "Insert Query: ", t_str
        # exit()

        res = None
        try:
            # print "debug: ", t_str
            self._client.send(t_str)
            insert_id = self._client.insert_id()
            res = self._client.commit()
            if res is None:
                res = insert_id
        except Exception, e:
            print "DB Insert Fail: {0} {1}".format(e, t_str)

        return res

    def get_values(self, columns, condition, limit=""):

        com_header = "SELECT "
        t_str = com_header

        for id in range(0, len(columns)):
            if id < (len(columns) - 1):
                t_str += columns[id] + ", "
            else:
                t_str += columns[id] + " "

        t_str += "FROM " + self._table_name + " "
        if condition != "":
            t_str += "WHERE " + condition

        if limit != "":
            t_str += limit

        return self._client.send(t_str)

    def get_count(self, condition):

        com_header = "SELECT count(*) "
        t_str = com_header
        t_str += "FROM " + self._table_name

        if condition != "":
            t_str += " WHERE " + condition

        return self._client.send(t_str)

    def clear_table(self):

        t_str = "DELETE FROM " + self._table_name

        return self._client.send(t_str)

    def exist(self, attr, value):
        condition = attr + "=" + value
        res = self.get_count(self._table_name, condition)
        return res

    def exist_in_pattern(self, attr, value):
        condition = attr + " Like " + value
        res = self.get_count(self._table_name, condition)
        return res

    def update(self, attr, value, condition):

        t_str = "UPDATE " + self._table_name + " "
        t_str += "SET " + attr + "=" + value + " "
        t_str += "WHERE " + condition

        return self._client.send(t_str)

    def delete(self, condition):
        t_str = "DELETE FROM " + self._table_name + " WHERE " + condition
        return self._client.send(t_str)


class MySQLClient(object):
    """

    """

    def __init__(self, user, password, host, db):
        self._user = user
        self._password = password
        self._host = host
        self._db = db

        self._con = None
        self._cur = None

    @property
    def db_name(self):
        return self._db

    def connect(self):
        """Connect to DB.

        :return: None
        """
        self._con = MySQLdb.connect(
            user=self._user,
            passwd=self._password,
            host=self._host,
            db=self._db,
            use_unicode=True,
            charset="utf8")
        self._cur = self._con.cursor(cursorclass=MySQLdb.cursors.SSCursor)
        uds.logging.info("Connect to MySQL. db_name=%s", self._db)

    def disconnect(self):
        """Disconnect DB.

        :return: None
        """
        self._cur.close()
        self._con.close()

    def send(self, query):
        """Send SQL statement.

        :param query: SQL statement
        :return: response of execute query
        """
        try:
            # print "Query:", query
            '''
            if query.find("INSERT") != -1:
                import os
                f = open('sql_log_{0}.txt'.format(os.getpid()), 'a')
                f.write("{0}\n".format(query))
                f.close()'''
            self._cur.execute(query)
            res = self._cur.fetchall()
        except Exception, e:
            uds.logging.error('sql:%s,\nmessage:%s', query, e)
            return []
        return res

    def commit(self):
        """Commit connection.

        :return: response of commit
        """
        return self._con.commit()

    def insert_id(self):
        return self._con.insert_id()


def try_create_database(user_name, password, host_name, db_name):
    """Create database if not exist.

    :param user_name:
    :param password:
    :param host_name:
    :param db_name:
    :return: None
    """
    con = MySQLdb.connect(user=user_name,
                          passwd=password,
                          host=host_name,
                          use_unicode=True,
                          charset="utf8")
    cur = con.cursor(cursorclass=MySQLdb.cursors.SSCursor)

    cur.execute('create database if not exists ' + db_name)
    cur.execute('use ' + db_name)
    print "Try to create database. db_name=" + db_name  # Not use uds.logging


def try_create_m2m_table(client, table_name, m2m_data):
    """Create M2MData table, if not exist.

    Query example::

        CREATE TABLE `RainSensor` (
            `id` bigint(20) NOT NULL AUTO_INCREMENT,
            `pointid` varchar(100) DEFAULT NULL,
            `time` datetime DEFAULT NULL,
            `prefname` varchar(100) DEFAULT NULL,
            `pointname` varchar(100) DEFAULT NULL,
            `value` float DEFAULT NULL,
            `value_unit` varchar(100) DEFAULT NULL,
            `geo_loc` geometry NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `time_loc` (`pointid`,`time`),
            KEY `idx_pointid` (`pointid`),
            KEY `idx_time` (`time`),
            KEY `idx_prefname` (`prefname`),
            KEY `idx_pointname` (`pointname`),
            KEY `idx_value` (`value`),
            SPATIAL KEY `idx_geo_loc` (`geo_loc`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8

    :param client:
    :param table_name:
    :param m2m_data:
    :return: None, or response of execute query
    """
    assert m2m_data.size != 0

    if check_table(client, table_name):
        return

    columns = '`time` datetime DEFAULT NULL,'
    columns += '`timezone` varchar(10) DEFAULT NULL,'
    columns += '`MySQLIndex` bigint(20) NOT NULL AUTO_INCREMENT,'
    keys = ''

    # Create columns for datum_values
    for columnName, data in m2m_data[0].items():
        keys = keys + 'KEY `idx_{columnName}` (`{columnName}`),'.format(columnName=columnName)
        if columnName == 'time':
            continue
        columns = columns + '`{columnName}` {type} DEFAULT NULL,'.format(columnName=str(columnName),
                                                                         type=_type_to_string(data))
    # Create columns for device_info
    for columnName, data in m2m_data.device_info.items():
        keys = keys + 'KEY `idx_{columnName}` (`{columnName}`),'.format(columnName=columnName)
        if columnName == 'latitude' or columnName == 'longitude':
            columns = columns + '`{columnName}` decimal(13,10) NOT NULL,'.format(columnName=str(columnName))
        else:
            columns = columns + '`{columnName}` {type} DEFAULT NULL,'.format(columnName=str(columnName),
                                                                             type=_type_to_string(data))
    # Create columns for data_units
    for columnName, data in m2m_data.data_units.items():
        if columnName in ['time', 'longitude', 'latitude']:
            continue
        columns = columns + '`unit_{columnName}` {type}  NULL,'.format(columnName=str(columnName),
                                                                       type=_type_to_string(data))
        pass

    # Create columns for m2m_info
    for columnName, data in m2m_data.info_summary.items():
        keys = keys + 'KEY `idx_{columnName}` (`{columnName}`),'.format(columnName=columnName)
        columns = columns + '`{columnName}` {type}  NULL,'.format(columnName=str(columnName),
                                                                  type=_type_to_string(data))
        pass

    query = 'CREATE TABLE `{0}` ('.format(table_name)
    query += columns
    query += keys
    query += 'PRIMARY KEY (`MySQLIndex`),'
    query += 'UNIQUE KEY `time_loc` (`time`, `latitude`, `longitude`)  USING BTREE'
    query += ') ENGINE=MyISAM DEFAULT CHARSET=utf8'

    result = client.send(query)
    return result


def check_table(client, table_name):
    """

    :param client:
    :param table_name:
    :return:
    """
    if (table_name, ) in show_tables(client):
        return True
    else:
        return False


def show_tables(client):
    """

    :param client:
    :return: response of execute query
    """
    query = 'SHOW TABLES FROM {db}'.format(db=client.db_name)

    return client.send(query)


def _type_to_string(data):
    if isinstance(data, int) or isinstance(data, float) or isinstance(data, long) or isinstance(data, complex):
        return 'float'
    else:
        return 'VARCHAR(200)'