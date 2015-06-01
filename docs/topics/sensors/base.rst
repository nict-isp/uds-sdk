Sensor Class
============

.. contents::
   :depth: 2

**Related Topics**
    :API Reference: :ref:`sensors-api` » :class:`~uds.sensors.base.Sensor`
    :Example:        N/A

:class:`~uds.sensors.base.Sensor` class is the common (base) template,
and other sensor template classes extends Sensor class.
Sensor class has basic methods
:meth:`~uds.sensors.base.Sensor.check`,
:meth:`~uds.sensors.base.Sensor.filter` and
:meth:`~uds.sensors.base.Sensor.store` that is previously implemented.

To implement *MySensor* class that inherits from the Sensor class,
configure runtime parameters and override methods as follows.

.. code-block:: python

    from uds.sensors.base import Sensor

    class MySensor(Sensor):
        def __init__(self, project_home):
            super(MySensor, self).__init__(project_home)

            # ~~~ Initialize sensor parameters here ~~~

            pass

        # Method overriding (mandatory)
        def fetch(self):...

        # Method overriding (mandatory)
        def parse(self, source):...

        # Method overriding (optional)
        def before_cycle(self):...

        # Method overriding (optional)
        def after_cycle(self):...

        # Method overriding (optional)
        def open(self):...

        # Method overriding (optional)
        def close(self):...

        # Method overriding (not recommended)
        def check(self, m2m_data_list):...

        # Method overriding (not recommended)
        def filter(self, m2m_data_list):...

        # Method overriding (not recommended)
        def store(self, m2m_data_list):...


.. _base-params-guide:

Configuring Basic Parameters
----------------------------

Set the following basic parameters as Sensor class properties.

===  ==================================================== ========= ===================
No.  Item                                                 Required? Description
===  ==================================================== ========= ===================
1.   :attr:`~uds.sensors.base.Sensor.sensor_name`         Yes       | The sensor’s name.
                                                                    | This is used in output filenames
                                                                    | and as the “title” attribute in M2M data.
2.   :attr:`~uds.sensors.base.Sensor.time_offset`         No        | The time zone. When M2M data is output, the time
                                                                    | is adjusted according to this time zone.
                                                                    | Default value ‘+00:00’
===  ==================================================== ========= ===================

Sample configuration:

.. code-block:: python

    self.sensor_name = 'MySensor'
    self.time_offset = '+0900'


.. _m2m-info-guide:

Configuring M2M Metadata
------------------------

Set information required in output M2M data via the following Sensor class properties.
For information on the M2M data format specifications, see :doc:`/refs/m2m/index` .

===  ==================================================== ========= ===================
No.  Item                                                 Required? Description
===  ==================================================== ========= ===================
3.   | :attr:`~uds.sensors.base.Sensor.m2m_info`          | ---     |
　   | 　　['formatVersion']                              | Yes     | The version of the M2M data format.
　   | 　　['srcContact']                                 | No      | Contact information for the data source.
　   | 　　['createdContact']                             | Yes     | Contact information for the data’s author.
　   | 　　['device']                                     | ---     | The sensor's device information.
　   | 　　　　['id']                                     | No      | Default value: None
　   | 　　　　['ownership']                              | No      | Default value: None
　   | 　　　　['ipaddress']                              | No      | Default value: None
　   | 　　　　['name']                                   | No      | Default value: None
　   | 　　　　['serial_no']                              | No      | Default value: None
　   | 　　　　['capability']                             | ---     | The sensor data's update frequency.
　   | 　　　　　　['frequency']                          | No      | Default value: None
　   | 　　　　　　['type']                               | No      | Default value: None
　   | 　　　　　　['count']                              | No      | Default value: None
　   | 　　　　　　['public']                             | No      | Default value: None
　   | 　　['security']                                   | No      | Security metadata.
　   | 　　['tag']                                        | No      | Arbitrary user-specified tag metadata.
===  ==================================================== ========= ===================


Sample configuration:

..  code-block:: python

    self.m2m_info = {
        'formatVersion': '1.02',
        'srcContact': '',
        'createdContact': 'Test User<testuser@example.com>',
        'tag': '',
        'device': {
            'capability': {
                'frequency': {
                    'type': 'seconds',
                    'count': 10
                }
            }
        }
    }

.. _m2m-data-schema-guide:

Configuring the M2M Data Schema
-------------------------------

Define the schema of the M2M data section via the following Sensor class properties.

===  ==================================================== ========= ===================
No.  Item                                                 Required? Description
===  ==================================================== ========= ===================
4.   | :attr:`~uds.sensors.base.Sensor.m2m_data_schema`   | Yes     | Definition of the M2M data section’s schema.
　   | 　　['type']                                       | Yes     | The data type.
     |                                                    |         | -- 'numeric' for numbers
     |                                                    |         | -- 'string' for strings
　   | 　　['name']                                       | Yes     | The data's name.
　   | 　　['unit']                                       | No      | The units in which the data is measured.
===  ==================================================== ========= ===================

Sample configuration:

..  code-block:: python

    self.m2m_data_schema = [
        {'type': 'string', 'name': 'time'},
        {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
        {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
        {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
        {'type': 'numeric', 'name': 'rainfall', 'unit': 'mm'},
        {'type': 'string', 'name': 'city_name'},
        {'type': 'string', 'name': 'station_name'}
    ]


.. _store-params-guide:

Configuring Output Location Parameters
--------------------------------------

Set the parameters required for M2M output data via the following Sensor class properties.

===  ==================================================== ========= ====================================================
No.  Item                                                 Required? Description
===  ==================================================== ========= ====================================================
5.   | :attr:`~uds.sensors.base.Sensor.filter_type`       | No      | Selects the type of filter to apply.
     |                                                    |         | Default value: 'time_order_filter'

6.   | :attr:`~uds.sensors.base.Sensor.store_type`        | No      | Selects the type of output location.
     |                                                    |         | Default value: ‘file’

7.   | :attr:`~uds.sensors.base.Sensor.store_params`      | ---     | Information on the output location.

　   | 　　['mysql']                                      | Yes     | Information for MySQL output.
     |                                                    |         | (Required when store_type is 'mysql')

　   | 　　　　['user']                                   |         | Username for MySQL connections.

　   | 　　　　['password']                               |         | Password for MySQL connections.

　   | 　　　　['host']                                   |         | Hostname for MySQL connections.

　   | 　　　　['db']                                     |         | Database name for MySQL connections.

　   | 　　　　['table_name']                             |         | Table name for storing data.
     |                                                    |         | If this parameter is none, **sensor_name**
     |                                                    |         | parameter is used for the table name.

　   | 　　['evwh']                                       | Yes     | Information for EventWarehouse output.
     |                                                    |         | (Required when store_type is 'evwh')

　   | 　　　　['host']                                   |         | Hostname for EventWarehouse connections.

　   | 　　　　['port']                                   |         | Port number for EventWarehouse connections.
　   | 　　　　['table_name']                             |         | Table name for storing data.
     |                                                    |         | If this parameter is none, **sensor_name**
     |                                                    |         | parameter is used for the table name.

　   | 　　['scn']                                        | Yes     | Information for sending data via SCN.
     |                                                    |         | (Required when store_type is 'scn')

　   | 　　　　['category']                               |         | 　

　   | 　　　　['type']                                   |         | 　
===  ==================================================== ========= ====================================================

Sample configuration:

.. code-block:: python

    self.store_params = {
        'mysql': {
            'user': 'testuser',
            'password': 'testuser',
            'host': 'mysql-server.example.com',
            'db': 'UDSEventData'
        },
        'evwh': {
            'host': 'evwh-server.example.com',
            'port': 12345
        }
    }

Overriding the fetch Method
---------------------------

Override the Sensor class's abstract :meth:`~uds.sensors.base.Sensor.fetch` method
with an implementation that retrieves data.

Your implementation should:

#.  Retrieve content with the desired data from the data source.

#.  Package the retrieved content into an object and return it.
    The returned object may be of any type.

Sample implementation:

.. code-block:: python

    import urllib2
    def fetch():
        """ Fetch html content from static URL, and return it.
        """
        url = 'http://www.example.com/test/data'
        response = urllib2.urlopen(urllib2.Request(url))
        html_text = response.read()
        return html_text

Overriding the parse Method
---------------------------

Override the Sensor class’s abstract :meth:`~uds.sensors.base.Sensor.parse` method
with an implementation that extracts data.

Your implementation should:

#.  Accept the fetch() method’s return value via the *source* argument.

#.  Extract data from *source*.

#.  Store the extracted data in :class:`uds.data.M2MData` objects.
    For more information on using M2MData objects, see :doc:`/topics/data` .

#.  Return the list of M2MData objects.

Sample implementation:

.. code-block:: python

    def parse(source):
        """ Extract data1、data2、data3 from HTML text and return it.
        """
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()

        datum1 = self._extract_datum1(source)
        m2m_data.append(datum1)
        datum2 = self._extract_datum2(source)
        m2m_data.append(datum2)
        datum3 = self._extract_datum3(source)
        m2m_data.append(datum3)

        m2m_data.append(datum)
        m2m_data_list.append(m2m_data)
        return m2m_data_list

Overriding Pre- and Post-Processing Methods (Optional)
------------------------------------------------------

You can override the Sensor class's :meth:`~uds.sensors.base.Sensor.open` method
to add processing before the crawl cycle begins.
Always call the parent class's open() method when you override it.

.. code-block:: python

    def open():
        super(MySensor, self).open()
        # ~~~ Write optional code here ~~~

You can override the Sensor class's :meth:`~uds.sensors.base.Sensor.close` method
to add processing after the crawl cycle begins.
Always call the parent class's close() method when you override it.

.. code-block:: python

    def close():
        super(MySensor, self).close()
        # ~~~ Write optional code here ~~~

You can override the Sensor class's :meth:`~uds.sensors.base.Sensor.before_cycle` method
to add processing at the beginning of a crawl cycle.
Always call the parent class's before_cycle() method when you override it.

.. code-block:: python

    def before_cycle():
        super(MySensor, self).before_cycle()
        # ~~~ Write optional code here ~~~

You can override the Sensor class's :meth:`~uds.sensors.base.Sensor.after_cycle` method
to add processing at the end of a crawl cycle.
Always call the parent class's after_cycle() method when you override it.

.. code-block:: python

    def before_cycle():
        super(MySensor, self).after_cycle()
        # ~~~ Write optional code here ~~~

Overriding Implemented Methods (Not Recommended)
------------------------------------------------

The Sensor class implements the following methods that you can override to customize their behavior.

* :meth:`~uds.sensors.base.Sensor.filter`

* :meth:`~uds.sensors.base.Sensor.check`

* :meth:`~uds.sensors.base.Sensor.store`

If you do override these methods, however,
you will no longer be able to use the Sensor class’s corresponding features
and must therefore implement them carefully.

Example Implementation
----------------------

:doc:`/refs/examples/http_sensor`