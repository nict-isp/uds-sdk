TwitterSensor Class
===================

.. contents::
   :depth: 2

**Related Topics**
    :API Reference: :ref:`sensors-api` » :class:`~uds.sensors.twitter.TwitterSensor`
    :Example:        :doc:`/refs/examples/twitter_sensor`

:class:`~uds.sensors.twitter.TwitterSensor` Fetches Tweet data
from Twitter using the Twitter Streaming APIs.
To implement your own sensor class that extends the TwitterSensor class,
configure runtime parameters and override methods as follows.

.. code-block:: python

    from uds.sensors.twitter import TwitterSensor

    class MyTwitterSensor(TwitterSensor):

        def __init__(self, project_home):
            super(MyTwitterSensor, self).__init__(project_home)

            # ~~~ Initialize sensor parameters here ~~~

            pass

        # Method overriding (mandatory)
        def parse_data(self, data):...

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

Configuring Authentication Parameters
-------------------------------------

To fetch data from Twitter,
you must connect to the Twitter Streaming API endpoints with OAuth credentials.
Configure the following parameters as your OAuth credentials.

===  ==================  =============
No.  Parameter           Description
===  ==================  =============
1.   consumer_key        The consumer key for a registered Twitter application.
2.   consumer_secret     The consumer secret for a registered Twitter application.
3.   access_key          An access token issued on behalf of a Twitter account for your application.
4.   access_secret       A token secret issued on behalf of a Twitter account for your application.
===  ==================  =============

Sample implementation:

.. code-block:: python

    self.set_auth_params(
        consumer_key='YOUR_CONSUMER_KEY',
        consumer_secret='YOUR_CONSUMER_SECRET',
        access_key='YOUR_ACCESS_KEY',
        access_secret='YOUR_ACCESS_SECRET'
    )



Configuring a Location Filter
-----------------------------

Configure a location filter to only collect Tweet data within a specified geographical area.

Sample implementation:

.. code-block:: python

    self.location_filter = [122.933611, 20.425277, 153.986388, 45.557777]


Configuring a Keyword Filter
----------------------------

Configure a keyword filter to only collect Tweet data that includes the specified keywords.
As shown below, specify keywords as a list of values and the resulting search will combine them with logical OR operators.
Within each individual list element,
a comma functions as a logical OR operator and a space functions as a logical AND operator.

Sample implementation:

.. code-block:: python

    self.keyword_filter = ['rain Rain', 'typhoon hurricane', 'Japan,USA']


Configuring a Japanese Keyword Filter
-------------------------------------

Configure a Japanese keyword filter to only collect Tweet data
that includes the specified Japanese keywords.
As shown below, specify keywords as a list of values and the resulting search will combine them with logical OR operators.

Sample implementation:

.. code-block:: python

    self.japanese_keyword_filter = ['雨', '風', '雪', '雲', 'くもり', '嵐', '暑', '寒']

Overriding the parse_data Method
--------------------------------

Override the TwitterSensor class’s abstract :meth:`~uds.sensors.twitter.TwitterSensor.parse_data`
method to implement the data extraction process.

Your implementation should:

#.  Accept a response from the Twitter Streaming APIs as a dictionary in the first argument (*data*).

#.  Extract the desired Tweet data from the *data* variable.

#.  Store the extracted data in :class:`~uds.data.M2MData` objects.

#.  Return the list of M2MData objects.

Sample implementation:

.. code-block:: python

    def parse_data(self, data):
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()

        # Extract the desired Tweet data from the data variable.
        datum = {}
        datum['time'] = data['created_at']
        datum['latitude'] = data['geo']['coordinates'][0]
        datum['longitude'] = data['geo']['coordinates'][1]
        datum['altitude'] = None
        datum['id_str'] = data['id_str']
        datum['tweet'] = data['text']

        m2m_data.append(datum)
        m2m_data_list.append(m2m_data)
        return m2m_data_list

TwitterSensor Behavior
----------------------

*   collects filtered Tweet data if you have configured a filter
*   fetches sample data provided by Twitter if you have not configured a filter
*   only fetches geotagged tweets from Twitter’s sample data


Example Implementation
----------------------

:doc:`/refs/examples/twitter_sensor`
