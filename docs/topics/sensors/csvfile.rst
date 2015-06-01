CSVFileSensor Class
===================

.. contents::
   :depth: 2

**Related Topics**
    :API Reference: :ref:`sensors-api` » :class:`~uds.sensors.csvfile.CSVFileSensor`
    :Example:        :doc:`/refs/examples/csvfile_sensor`

:class:`~uds.sensors.csvfile.CSVFileSensor` reads local CSV file data.
To implement your own sensor class that extends the CSVFileSensor class,
configure runtime parameters and override methods as follows.

.. code-block:: python

    from uds.sensors.csvfile import CSVFileSensor

    class MyCSVFileSensor(CSVFileSensor):

        def __init__(self, project_home):
            super(MyCSVFileSensor, self).__init__(project_home)

            # ~~~ Initialize sensor parameters here ~~~

            pass

        # Method overriding (mandatory)
        def parse_rows(self, reader, file_path):...

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

Configuring Parameters Unique to the CSVFileSensor Class
--------------------------------------------------------

Configure the following parameter as an CSVFileSensor class property.

====  ==============================================================  =========  =================================================================
No.   Item                                                            Required?  Description
====  ==============================================================  =========  =================================================================
1.    | :attr:`~uds.sensors.csvfile.CSVFileSensor.interval`           | No       | The interval at which to retrieve data from the data source.
      |                                                               |          | The sensor will access the data source once
      |                                                               |          | during each interval of the specified number of seconds.
      |                                                               |          | Default value: 0

2.    | :attr:`~uds.sensors.csvfile.CSVFileSensor.file_list`          | Yes      | List of reading CSV file paths.
====  ==============================================================  =========  =================================================================

Sample configuration:

.. code-block:: python

    # Set interval to 10 second.
    self.interval = 10

    # Append file path to list.
    self.file_list.append('./file1.csv')
    self.file_list.append('./file2.csv')
    self.file_list.append('./file3.csv')

Overriding the parse_raws Method
---------------------------------

Override the CSVFileSensor class's abstract
:meth:`~uds.sensors.csvfile.CSVFileSensor.parse_rows` method
to implement the data extraction process.

Your implementation should:

#.  Accept fetched table rows as a list in the first argument (*rows*),
    and the file's path in the second argument (*file_path*).

#.  Extract the desired data from the *rows* variable.

#.  Store the extracted data in :class:`~uds.data.M2MData` objects.

#.  Return list of M2MData objects.

Sample implementation:

.. code-block:: python

    def parse_rows(self, rows, file_path):
        m2m_data_list = []
        m2m_data = self.data_builder.create_data()

        for row in reader:
            datum = {}
            datum['data1'] = rows['column1']
            datum['data2'] = rows['column2']
            datum['data2'] = rows['column3']
            m2m_data.append(datum)

        m2m_data_list.append(m2m_data)
        return m2m_data_list

Example Implementation
----------------------

:doc:`/refs/examples/csvfile_sensor`