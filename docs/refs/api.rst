=============
API Reference
=============
This part of the documentation covers user interfaces of UDS.
For parts where UDS depends on external libraries, we provide links to the canonical documentation.

.. _sensors-api:

Sensors
=======

Sensor Class
------------

.. autoclass:: uds.sensors.base.Sensor
    :show-inheritance:

    Properties
        Properties such as sensor's runtime parameters and utility objects are provided.

        .. autoattribute:: uds.sensors.base.Sensor.start_time
        .. autoattribute:: uds.sensors.base.Sensor.project_home
        .. autoattribute:: uds.sensors.base.Sensor.config_dir_path
        .. autoattribute:: uds.sensors.base.Sensor.log_dir_path
        .. autoattribute:: uds.sensors.base.Sensor.out_dir_path
        .. autoattribute:: uds.sensors.base.Sensor.cache_dir_path

        .. autoattribute:: uds.sensors.base.Sensor.sensor_name
        .. autoattribute:: uds.sensors.base.Sensor.time_offset
        .. autoattribute:: uds.sensors.base.Sensor.m2m_info
        .. autoattribute:: uds.sensors.base.Sensor.m2m_data_schema
        .. autoattribute:: uds.sensors.base.Sensor.primary_keys
        .. autoattribute:: uds.sensors.base.Sensor.config
        .. autoattribute:: uds.sensors.base.Sensor.filter_type
        .. autoattribute:: uds.sensors.base.Sensor.store_type
        .. autoattribute:: uds.sensors.base.Sensor.store_params
        .. autoattribute:: uds.sensors.base.Sensor.time_record_enabled
        .. autoattribute:: uds.sensors.base.Sensor.log_file_enabled
        .. autoattribute:: uds.sensors.base.Sensor.log_params
        .. autoattribute:: uds.sensors.base.Sensor.ignore_confirmation

        .. autoattribute:: uds.sensors.base.Sensor.data_builder
        .. autoattribute:: uds.sensors.base.Sensor.geocoder

    Methods
        Methods corresponding to data sensing primary steps.
        Some of these methods can be overridden.

        .. automethod:: uds.sensors.base.Sensor.run
        .. automethod:: uds.sensors.base.Sensor.open
        .. automethod:: uds.sensors.base.Sensor.close
        .. automethod:: uds.sensors.base.Sensor.before_cycle
        .. automethod:: uds.sensors.base.Sensor.after_cycle
        .. automethod:: uds.sensors.base.Sensor.fetch
        .. automethod:: uds.sensors.base.Sensor.parse
        .. automethod:: uds.sensors.base.Sensor.check
        .. automethod:: uds.sensors.base.Sensor.filter
        .. automethod:: uds.sensors.base.Sensor.store

HttpSensor Class
----------------

.. autoclass:: uds.sensors.http.HttpSensor
    :show-inheritance:

    .. autoattribute:: uds.sensors.http.HttpSensor.interval

    .. automethod:: uds.sensors.http.HttpSensor.create_request
    .. automethod:: uds.sensors.http.HttpSensor.parse_content

TwitterSensor Class
-------------------

.. autoclass:: uds.sensors.twitter.TwitterSensor
    :show-inheritance:

    .. autoattribute:: uds.sensors.twitter.TwitterSensor.URI

    .. automethod:: uds.sensors.twitter.TwitterSensor.set_auth_params
    .. autoattribute:: uds.sensors.twitter.TwitterSensor.location_filter
    .. autoattribute:: uds.sensors.twitter.TwitterSensor.keyword_filter
    .. autoattribute:: uds.sensors.twitter.TwitterSensor.japanese_keyword_filter

    .. automethod:: uds.sensors.twitter.TwitterSensor.parse_data

IEEE1888Sensor Class
--------------------

.. autoclass:: uds.sensors.ieee1888.IEEE1888Sensor
    :show-inheritance:

    .. autoattribute:: uds.sensors.ieee1888.IEEE1888Sensor.interval
    .. autoattribute:: uds.sensors.ieee1888.IEEE1888Sensor.wsdl_url

    .. automethod:: uds.sensors.ieee1888.IEEE1888Sensor.create_query_keys
    .. automethod:: uds.sensors.ieee1888.IEEE1888Sensor.parse_response

MySQLSensor Class
-----------------

.. autoclass:: uds.sensors.mysql.MySQLSensor
    :show-inheritance:

    .. autoattribute:: uds.sensors.mysql.MySQLSensor.interval
    .. autoattribute:: uds.sensors.mysql.MySQLSensor.mysql_fetch_params

    .. automethod:: uds.sensors.mysql.MySQLSensor.create_query
    .. automethod:: uds.sensors.mysql.MySQLSensor.parse_rows

CSVFileSensor Class
---------------------

.. autoclass:: uds.sensors.csvfile.CSVFileSensor
    :show-inheritance:

    .. autoattribute:: uds.sensors.csvfile.CSVFileSensor.interval
    .. autoattribute:: uds.sensors.csvfile.CSVFileSensor.file_list

    .. automethod:: uds.sensors.csvfile.CSVFileSensor..parse_rows


.. _data-api:

Data Object
===========

M2MData
-------

.. autoclass:: uds.data.M2MData
    :show-inheritance:
    :members:

M2MDataV101
-----------

.. autoclass:: uds.data.M2MDataV101
    :show-inheritance:
    :members:

M2MDataV102
-----------

.. autoclass:: uds.data.M2MDataV102
    :show-inheritance:
    :members:

M2MDataVisitor
--------------

.. autoclass:: uds.data.M2MDataVisitor
    :show-inheritance:
    :members:

M2MDataBuilder
--------------

.. autoclass:: uds.data.build.M2MDataBuilder
    :show-inheritance:
    :members:

M2MDataCommitter
----------------

.. autoclass:: uds.data.commit.M2MDataCommitter
    :show-inheritance:
    :members:

M2MDataChecker
--------------

.. autoclass:: uds.data.check.M2MDataChecker
    :show-inheritance:
    :members:


.. _config-api:

Configuration
=============

.. autoclass:: uds.config.Config
    :show-inheritance:
    :members:

.. automodule:: uds.config.default_config
    :members:


.. _logging-api:

Logging
=======

.. automodule:: uds.logging
    :members:


.. _utils-api:

Utilities
=========

.. automodule:: uds.utils.string
    :members:

Geocoders
---------

.. autoclass:: uds.utils.geocoders.Geocoder
    :show-inheritance:

    .. automethod:: uds.utils.geocoders.Geocoder.str_to_loc_list


.. _tools-api:

Tools
=====

Command Line Tool
-----------------

.. automodule:: uds.tools.cli
    :members:


.. _exceptions-api:

Exceptions
==========

.. automodule:: uds.exceptions


.. _contrib-api:

Extra Package
=============

.. automodule:: uds.contrib
