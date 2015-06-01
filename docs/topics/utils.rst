Using Utilities
===============

.. contents::
    :depth: 3

**API Reference**
    * :ref:`utils-api`


String Parsing Utilities
------------------------

Your sensor implementation can use the functions defined in the
:attr:`uds.utils.string` module for string parsing.

Parsing Strings into Numbers
::::::::::::::::::::::::::::

Use the :meth:`~uds.utils.string.try_parse_to_numeric` function.

.. code-block:: python

        import uds.utils.string as string_util

        numeric_value = string_util.try_parse_to_numeric('12.24')

Parsing a Date/Time String into an ISO 8601 Formatted String
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Use the :meth:`~uds.utils.string.try_parse_to_datetime` function.

.. code-block:: python

        import uds.utils.string as string_util

        iso_datetime = string_util.try_parse_to_datetime('2015/03/31 10:20:30')

Removing Unnecessary Characters from Text
:::::::::::::::::::::::::::::::::::::::::

Use :meth:`~uds.utils.string.try_parse_to_string` function.

.. code-block:: python

        import uds.utils.string as string_util

        valid_text = string_util.try_parse_to_string("invalid u'\xa0' text")


Geocoding Utilities
-------------------

You can use the :class:`~uds.utils.geocoders.Geocoder` class
to get latitude and longitude coordinates from addresses,
place names, and other information.
Get a Geocoder object from your sensor's :attr:`~uds.sensors.base.Sensor.geocoder` property.

.. code-block:: python

    # Get latitude and longitude coordinates from country name.
    loc_list1 = self.geocoder.str_to_loc_list("Korea")
    print "longitude1=" + loc_list2["longitude"]
    print "latitude1=" + loc_list2["latitude"]

    # Get latitude and longitude coordinates from name of building.
    loc_list2 = self.geocoder.str_to_loc_list("Kobe Station")
    print "longitude2=" + loc_list2["longitude"]
    print "latitude2=" + loc_list2["latitude"]

.. note::

    *   Geocoder class has geocoded an address or place name,
        it caches the result under the **<PROJECT_DIR>/_cache** directory.
