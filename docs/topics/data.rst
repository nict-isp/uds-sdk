Using Data Objects
==================

.. contents::
    :depth: 2

**API Reference**
    * :ref:`data-api`


A User-Defined Sensor (UDS) converts the data it crawls into :class:`~uds.data.M2MData` objects.
Follow these steps to create M2MData objects in *MySensor* implementation.

#.  Use Sensor class properties to configure metadata for initializing M2MData objects.

#.  Use an M2MDataBuilder object to create an M2MData object.

#.  Add required device information and data values to the M2MData object.


.. note::
   For information on the M2M data format specifications, see :doc:`/refs/m2m/index`.


Configuring Metadata for Initializing M2MData Objects
-----------------------------------------------------

While referring to implementation of :doc:`/topics/sensors/base`,
configure these four properties with metadata that will be used to initialize M2MData objects.

* :attr:`~uds.sensors.base.Sensor.sensor_name` 　-　 See :ref:`base-params-guide`.

* :attr:`~uds.sensors.base.Sensor.time_offset` 　-　 See :ref:`base-params-guide`.

* :attr:`~uds.sensors.base.Sensor.m2m_info` 　-　 See :ref:`m2m-info-guide`.

* :attr:`~uds.sensors.base.Sensor.m2m_data_schema` 　-　 See :ref:`m2m-data-schema-guide`.

Sample configuration:

.. code-block:: python

    class MySensor(Sensor):
        def __init__(self):
            # * * * snip * * *

            # Set basic parameters
            self.sensor_name = 'MySensor'
            self.time_offset = '+0900'

            # Set parameters for M2M Data
            self.m2m_info = {
                'formatVersion': '1.02',
                'srcContact': '',
                'createdContact': 'My Name<myname@example.com>',
                'tag': '',
                'device': {
                    'capability': {
                        'frequency': {
                            'type': 'minutes',
                            'count': 10
                        }
                    }
                }
            }
            self.m2m_data_schema = [
                {'type': 'datetime', 'name': 'time'},
                {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
                {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
                {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
                {'type': 'numeric', 'name': 'SO2', 'unit': 'ppm'},
                {'type': 'numeric', 'name': 'NO', 'unit': 'ppm'},
                {'type': 'numeric', 'name': 'NO2', 'unit': 'ppm'},
            ]
            self.primary_keys = ['time', 'longitude', 'latitude']

            # * * * snip * * *

Generating Data with M2MDataBuilder
-----------------------------------

You can access your sensor's :attr:`~uds.sensors.base.Sensor.data_builder` property
to use an :class:`~uds.data.build.M2MDataBuilder` object.
Create M2MData objects with the :meth:`~uds.data.build.M2MDataBuilder.create_m2m_data` method.

.. code-block:: python

    m2m_data = self.data_builder.create_m2m_data()


Adding Device Information to an M2MData Object
----------------------------------------------

Use the :attr:`~uds.data.M2MData.device_info` property
to configure device information for an M2MData object.

.. code-block:: python

    m2m_data.device_info['station_code'] = '123456789'
    m2m_data.device_info['station_name'] = 'tokyo'

Adding Data Value to an M2MData Object
--------------------------------------

Use the :meth:`~uds.data.M2MData.append` method to add data value to an M2MData object.

.. code-block:: python

    datum1 = {
        'value1': 0.1,
        'value2': 0.2,
        'value3': 0.3
    }
    m2m_data.append(datum1)

    datum2 = {
        'value1': 2.1,
        'value2': 2.2,
        'value3': 2.3
    }
    m2m_data.append(datum2)


Checking M2M Data
-----------------

You can use the following properties to access the data stored in an :class:`~uds.data.M2MData` object.

    * :attr:`~uds.data.M2MData.device_info` 　--　 *sensor_info* → *device_info* in the object's metadata section

    * :attr:`~uds.data.M2MData.data_values` 　--　 *data* → *values* in the object’s data section

    * :attr:`~uds.data.M2MData.dict` 　--　 All M2M data (both the metadata and data sections)

.. code-block:: python

    # Show device information
    import json
    print json.dumps(m2m_data.device_info, indent=2)


.. code-block:: python

    # Show data values
    import json
    print json.dumps(m2m_data.data_values, indent=2)

You can also specify an index to access the individual data values stored
in an :class:`~uds.data.M2MData` object one after the other.

.. code-block:: python

    # Show data values at the index of 0
    print m2m_data[0]

    # Show data values at the index of 1
    print m2m_data[1]

    # Show data values at the index of 2
    print m2m_data[2]