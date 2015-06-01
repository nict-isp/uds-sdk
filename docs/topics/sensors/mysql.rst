MySQLSensor Class
=================

.. contents::
   :depth: 2

**Related Topics**
    :API Reference: :ref:`sensors-api` » :class:`~uds.sensors.mysql.MySQLSensor`
    :Example:        :doc:`/refs/examples/mysql_sensor`

:class:`~uds.sensors.mysql.MySQLSensor` class reads MySQL data.
To implement your own sensor class that extends the MySQLSensor class,
configure runtime parameters and override methods as follows.

.. code-block:: python

    from uds.sensors.mysql import MySQLSensor

    class MyMySQLSensor(MySQLSensor):

        def __init__(self, project_home):
            super(MyMySQLSensor, self).__init__(project_home)

            # ~~~ Initialize sensor parameters here ~~~

            pass

        # Method overriding (mandatory)
        def create_query(self):...

        # Method overriding (mandatory)
        def parse_rows(self, rows):...

        # Method overriding (optional)
        def before_cycle(self):...

        # Method overriding (optional)
        def after_cycle(self):...

        # Method overriding (optional)
        def open(self):...

        # Method overriding (optional)
        def close(self):...

Configuring parameters Shared with the Sensor Class
---------------------------------------------------

Configure the following parameters just as you would for a Sensor class implementation.

* :ref:`base-params-guide`

* :ref:`m2m-info-guide`

* :ref:`m2m-data-schema-guide`

* :ref:`store-params-guide`

Configuring Parameters Unique to the MySQLSensor Class
------------------------------------------------------

Configure the following parameter as an MySQLSensor class property.

====  ==============================================================  =========  =================================================================
No.   Item                                                            Required?  Description
====  ==============================================================  =========  =================================================================
1.    | :attr:`~uds.sensors.mysql.MySQLSensor.interval`               | No       | The interval at which to retrieve data from the data source.
      |                                                               |          | The sensor will access the data source once
      |                                                               |          | during each interval of the specified number of seconds.
      |                                                               |          | Default value: 0
2.    | :attr:`~uds.sensors.mysql.MySQLSensor.mysql_fetch_params`     | --       |
　    | 　　['user']                                                  | Yes      | Username for MySQL connections.
　    | 　　['password']                                              | Yes      | Password for MySQL connections.
　    | 　　['host']                                                  | Yes      | Hostname or IP address for MySQL connections.
　    | 　　['db']                                                    | Yes      | Database name for MySQL connections.
====  ==============================================================  =========  =================================================================

Sample configuration:

.. code-block:: python

    # Set interval to 10 second.
    self.interval = 10

    # Set information of MySQL connection.
    self.mysql_fetch_params = {
        'user': 'testuser',
        'password': 'testuser',
        'host': 'mysql-server.example.com',
        'db': 'GeoSocialDatabase'
    }

Overriding the create_query Method
----------------------------------

Override the MySQLSensor class's abstract :meth:`~uds.sensors.mysql.MySQLSensor.create_query` method
with an implementation that creates query for reading data from MySQL.

Your implementation should:

#.  Create SQL SELECT statement to read desired data.

#.  Return the SQL statement.

Sample implementation:

.. code-block:: python

    def create_query(self):
        query  = 'SELECT NIES_code, SO2, NO, NO2 '
        query += 'FROM japan_airpollution_data'
        query += 'WHERE log_datetime="2013-04-01T12:00:00"'
        return query

The create_query() method is only called once per crawl cycle.
If you would like to change your query each time you read data,
your implementation should return a different value for each cycle.

Overriding the parse_rows Method
--------------------------------
Override the MySQLSensor class's abstract
:meth:`~uds.sensors.mysql.MySQLSensor.parse_rows` method
to implement the data extraction process.

Your implementation should:

#.  Accept fetched table rows as a list in the first argument (*rows*)

#.  Extract the desired data from the *rows* variable.

#.  Store the extracted data in :class:`~uds.data.M2MData` objects.

#.  Return list of M2MData objects.

Sample implementation:

.. code-block:: python

    def parse_rows(self, rows):
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()

        for row in rows:
            datum = {}
            datum['SO2'] = row['SO2']
            datum['NO'] = row['NO']
            datum['NO2'] = row['NO2']
            m2m_data.append(datum)

        m2m_data_list.append(m2m_data)
        return m2m_data_list

Example Implementation
----------------------

:doc:`/refs/examples/mysql_sensor`