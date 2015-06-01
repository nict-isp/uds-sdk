===================
HttpSensor Tutorial
===================

.. contents::
   :depth: 2

**Related Topics**
    :User's Guide:  :doc:`/topics/sensors/index` » :doc:`/topics/sensors/http`
    :API Reference:     :ref:`sensors-api` » :class:`~uds.sensors.http.HttpSensor`
    :Example:   :doc:`/refs/examples/http_sensor`



The test website (http://SAMPLE_DATA_LOCATION/sample-rainfall/)
implements a sensor that collects the rainfall data
and is one example of the kind of sensor that you can develop.
(Example data is available in examples/sample_rainfall directory.)

This tutorial will lead you through the following step-by-step instructions
for building your own sensor.

#.  Create a UDS project.

#.  Choose the appropriate sensor template and prepare a template script.

#.  Edit the template script to implement your sensor class (*MySensor*).

#.  Run *MySensor* and check its output data.

|

Creating a UDS Project
======================

First, open a shell prompt and create a new UDS project
for this tutorial with the following :attr:`uds` command.

::

    $ uds new-project uds-tutorial


This command generates a 'uds-tutorial' directory with the following files and subdirectories.

::

    uds-tutorial
        |─ _cache
        |─ _log
        |─ _out
        |─ conf
        |   └─ project_conf.py
        └─ examples
        |   └─ sensors
        |       |─ ExampleCSVFileSensor.py
        |       |─ ExampleHttpSensor.py
        |       └─ (Other examples)
        └─ udsimpl
            └─ sensors

※ In this document, the directory path of a uds project like 'uds-tutorial'
is described as **<PROJECT_HOME>** .


Creating *MySensor* Script
==========================

In this tutorial, we’ll choose a sensor template
that is optimized for scraping websites --- the :class:`~uds.sensors.http.HttpSensor` class ---
and then you'll implement *MySensor* class that inherits from it.

Run the following command to generate the sample sensor script file that you’ll be implementing.


::

    $ uds new-sensor -t HttpSensor ExampleHttpSensor

Take a look at the content of *<PROJECT_HOME>/udsimpl/sensors/ExampleHttpSensor.py* :

.. code-block:: python

    # -*- coding: utf-8 -*-
    import os
    from uds.sensors.http import HttpSensor


    class ExampleHttpSensor(HttpSensor):

        def __init__(self, project_home):
            super(ExampleHttpSensor, self).__init__(project_home)

            # ~~~ Initialize sensor parameters here ~~~

            pass

        # Method overriding (mandatory)
        def create_request(self):
            pass

        # Method overriding (mandatory)
        def parse_content(self, content, url):
            pass

        # * * * snip * * *


    def get_sensor(project_home):
        return ExampleHttpSensor(project_home)


    if __name__ == '__main__':
        PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        sensor = get_sensor(PROJECT_HOME)
        sensor.run()

In the following sections, you’ll edit this file to customize your sensor class.


Implementing *MySensor* Class
=============================

Parameter Setting 1 --- Configuring Basic Parameters
----------------------------------------------------

Add the following basic sensor information in the __init__() method.

#.  The sensor’s name.

    .. code-block:: python

        self.sensor_name = 'ExampleHttpSensor'

#.  The data's time zone. We'll use Japan's time zone offset (+0900) for this example.

    .. code-block:: python

        self.time_offset = '+0900'


#.  Set the interval at which the HttpSensor will periodically poll its data source.

    .. code-block:: python

        self.interval = 10  # 10 seconds

#.  Specify the location of the output data. We’ll choose a local file for this example.

    .. code-block:: python

        self.store_type = 'file'


Parameter Setting 2 --- Configuring Metadata on the Output
----------------------------------------------------------

Use a dictionary (:attr:`dict`) to add the following metadata to the output (:doc:`/topics/data`).

*   formatVersiion (Required) 　--　 The version of the output data format (M2M data format).

*   createdContact (Required) 　--　 Contact information for the data’s author.

*   tag (Optional) 　--　 Arbitrary user-specified tag metadata.

*   device ->capaility -> frequency -> type (Optional) 　--　 The data source’s update frequency.

*   device ->capaility -> frequency -> count(Optional) 　--　 The amount of data retrieved each cycle.

In the __init__() method:

.. code-block:: python

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

Parameter Setting 3 --- Defining the Output Data Schema
-------------------------------------------------------

Use a dictionary (:attr:`dict`) to define the following for each instance of data.

* name（Required） -- The data’s name.

* type（Required） -- The data’s type (similar to a JSON data type).

* unit（Optional） -- The units in which the data is measured.

In the __init__() method:

.. code-block:: python

    self.m2m_data_schema = [
        {'type': 'string', 'name': 'time'},
        {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
        {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
        {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
        {'type': 'numeric', 'name': 'rainfall', 'unit': 'mm'},
        {'type': 'string', 'name': 'city_name'},
        {'type': 'string', 'name': 'station_name'}
    ]

And use a list to define primary keys.

In the __init__() method:

.. code-block:: python

    self.primary_keys = ['time', 'longitude', 'latitude']

Method implementation 1 --- Specifying the Data Source’s URL
-------------------------------------------------------------

Override the HttpSensor class's abstract method
:meth:`uds.sensors.http.HttpSensor.create_request` with an implementation
that returns the URL of the HTML data that you want to retrieve.
This method is only called once per crawling cycle.

.. code-block:: python

    def __init__(self, project_home):
        # * * * snip * * *

        # Set url list.
        self._url_list = [
            'http://SAMPLE_DATA_LOCATION/sample-rainfall/pre1h/20140809T0900.html',
            'http://SAMPLE_DATA_LOCATION/sample-rainfall/pre1h/20140809T1000.html',
            'http://SAMPLE_DATA_LOCATION/sample-rainfall/pre1h/20140809T1100.html'
        ]

    def create_request(self):
        if len(self._url_list) == 0:
            # If url list is empty, abort crawling.
            self.abort()
            return None, None

        # Deque url from url list
        url = self._url_list.pop(0)
        return url, None

Method implementation 2 --- Implementing the Data Parsing Process
-----------------------------------------------------------------

Override the HttpSensor class's abstract method
:meth:`~uds.sensors.http.HttpSensor.parse_content` with an implementation
that extracts data from the retrieved HTML.
This method is only called once per crawling cycle.

#.  Create an :class:`~uds.data.M2MData` object for storing the parsed data.

    .. code-block:: python

        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()


#.  Import lxml and use it as an HTML parser.

    .. code-block:: python

        from lxml import etree

    .. code-block:: python

        element = etree.HTML(content)

#.  Extract data source time, and convert the (string) timestamp into an ISO 8601 formatted string,
    then save it to *sensing_time* variable.
    In the following example, we import datetime string parsing utility and use it.

    .. code-block:: python

        from uds.utils.string import try_parse_to_datetime

    .. code-block:: python

        # * * * snip * * *

        sensing_time = element.xpath('body/h1/text()')[0]
        match = re.match(u'(1時間降水量一覧表 )(.+)', sensing_time)
        if match:
            sensing_time = match.group(2)
            sensing_time = try_parse_to_datetime(sensing_time)
        else:
            uds.logging.error('[parse] Failed to parse time.')
            return m2m_data_list

        # * * * snip * * *

#.  Analyze the HTML for salient data.

    In the following example, we analyze the HTML for each row of the table
    stored in the *tr_list* variable and then save the extracted values.
    Import string parsing utilities and use it.

    .. code-block:: python

        from uds.utils.string import try_parse_to_string
        from uds.utils.string import try_parse_to_numeric

    .. code-block:: python

        # Parse table rows
        tr_list = element.xpath('body/table/tbody/tr')

        for tr in tr_list:
            datum = {}

            datum['time'] = sensing_time
            datum['city_name'] = try_parse_to_string(
                tr.xpath('td[1]/text()')[0]
            )
            datum['station_name'] = try_parse_to_string(
                tr.xpath('td[2]/text()')[0]
            )
            datum['rainfall'] = try_parse_to_numeric(
                tr.xpath('td[3]/text()')[0]
            )

            # * * * snip * * *

#.  Use the :class:`~uds.utils.geocoders.Geocoder` class to calculate
    latitude and longitude coordinates from addresses and other strings.
    And if succeed to geocode, store the extracted values in the M2MData object.

    In the following example, we convert the *city_name* and the *station_name*
    into latitude and longitude coordinates, which we then store *in m2m_data*.

    .. code-block:: python

        for tr in trList:
            # * * * snip * * *

            # Geocode address to latitude/longitude
            geo_word = datum['city_name'] + ' ' + datum['station_name']
            loc_list = self.geocoder.str_to_loc_list(geo_word)
            if loc_list is False:
                # If failed, ignore the data
                uds.logging.warning('[parse] Can not Location Data.')
                continue
            else:
                datum["latitude"] = loc_list["latitude"]
                datum["longitude"] = loc_list["longitude"]
                datum["altitude"] = None

                m2m_data.append(datum)


#.  Return list of the M2MData object.

    .. code-block:: python

        m2m_data_list.append(m2m_data)
        return m2m_data_list


Running *MySensor* Script
=========================

Run the script that you just implemented above from the command line.

::

    $ uds run udsimpl/sensors/ExampleHttpSensor.py

.. note::

    You can also run your script from the python command.

    ::

        $ cd <PROJECT_HOME>
        $ PYTHONPATH=. python udsimpl/sensors/ExampleHttpSensor.py


Checking the Output
===================

Output Data
-----------

Check the JSON output data saved to files under the

    *<PROJECT_HOME>/_out/m2m_data*

directory.

Logs
----

You can examine the logs (ExampleHttpSensor.log) saved in the

    *<PROJECT_HOME>/_log*

directory for debugging or other purposes.


Source Code Listing for This Tutorial
=====================================

:doc:`/refs/examples/http_sensor`
