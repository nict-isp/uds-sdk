HttpSensor Class
=================

.. contents::
   :depth: 2

**Related Topics**
    :Tutorial:       :doc:`/intro/tutorial/http_sensor`
    :API Reference: :ref:`sensors-api` » :class:`~uds.sensors.http.HttpSensor`
    :Example:        :doc:`/refs/examples/http_sensor`

:class:`~uds.sensors.http.HttpSensor` class crawls HTML content
from web pages and other sources using HTTP GET and POST methods.
To implement your own sensor class that extends the HttpSensor class,
configure runtime parameters and override methods as follows.

.. code-block:: python

    from uds.sensors.http import HttpSensor

    class MyHttpSensor(HttpSensor):

        def __init__(self, project_home):
            super(MyHttpSensor, self).__init__(project_home)

            # ~~~ Initialize sensor parameters here ~~~

            pass

        # Method overriding (mandatory)
        def create_request(self):...

        # Method overriding (mandatory)
        def parse_content(self, content, url):...

        # Method overriding (optional)
        def before_cycle(self):...

        # Method overriding (optional)
        def after_cycle(self):...

        # Method overriding (optional)
        def open(self):...

        # Method overriding (optional)
        def close(self):...


Configuring Parameters Shared with the Sensor Class
---------------------------------------------------

Configure the following parameters just as you would for a Sensor class implementation.

* :ref:`base-params-guide`

* :ref:`m2m-info-guide`

* :ref:`m2m-data-schema-guide`

* :ref:`store-params-guide`

Configuring Parameters Unique to the HttpSensor Class
-----------------------------------------------------

Configure the following parameter as an HttpSensor class property.

===  ==================================================== ========= ================================================================
No.  Item                                                 Required? Description
===  ==================================================== ========= ================================================================
1.   | :attr:`~uds.sensors.http.HttpSensor.interval`      | No      | The interval at which to retrieve data from the data source.
     |                                                    |         | The sensor will access the data source once
     |                                                    |         | during each interval of the specified number of seconds.
     |                                                    |         | Default value: 0
===  ==================================================== ========= ================================================================

Sample configuration:

.. code-block:: python

    # Get data once every 10 seconds
    self.interval = 3 * 60

Overriding the create_request Method
------------------------------------

Override the HttpSensor class’s abstract :meth:`~uds.sensors.http.HttpSensor.create_request` method
to specify how data will be fetched.

Your implementation should:

#.  Return the following values.

    -- The URL to the data source

    -- POST parameters

    If you don’t specify any POST parameters, data will be retrieved with an HTTP GET request;
    otherwise, data will be retrieved with an HTTP POST request.

Sample implementation:

.. code-block:: python

    def create_request(self):
        """ Return request to fetch html content from static URL.
        """
        url = 'http://www.example.com/test/data'
        return url, None

Overriding the parse_content Method
-----------------------------------

Override the HttpSensor class's abstract :meth:`~uds.sensors.http.HttpSensor.parse_content` method
to implement the data extraction process.

Your implementation should:

#.  Accept fetched content in the first argument (*content*)
    and the content’s URL in the second argument (*url*).

#.  Extract data from *content*.

#.  Store the extracted data in :class:`~uds.data.M2MData` objects.
    For more information on using M2MData objects, see :doc:`/topics/data`.

#.  Return the list of M2MData objects.

Sample implementation:

.. code-block:: python

    def parse(self, content, url):
        """Extract table first row data from HTML text and return it.
        """
        # Prepare M2MData object
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()
        m2m_data.dict['primary']['provenance']['source']['info'] = url

        # Parse contents by use of lxml
        element = etree.HTML(content)

        # Parse table first row
        tr_list = element.xpath('body/table/tbody/tr')
        tr = tr_list[0]

        datum = {}
        datum['city_name'] = try_parse_to_string(
            tr.xpath('td[1]/text()')[0]
        )
        datum['station_name'] = try_parse_to_string(
            tr.xpath('td[2]/text()')[0]
        )
        datum['rainfall'] = try_parse_to_numeric(
            tr.xpath('td[3]/text()')[0]
        )

        m2m_data.append(datum)
        m2m_data_list.append(m2m_data)
        return m2m_data_list

Example Implementation
----------------------

:doc:`/refs/examples/http_sensor`

