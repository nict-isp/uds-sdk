What's a User-defined Sensor?
=============================

A User-defined Sensor (UDS) is a tool that crawls web pages,
RSS feeds, Twitter, and various other data sources
to collect and manipulate event data containing time-space information.
This SDK provides libraries and tools for developing User-defined Sensors.


UDS Scrapes Event Data
----------------------

A UDS treats event data that has time of occurrence and site of occurrence
(longitude, latitude, altitude) information
e.g. rain fall data, traffic jam information, and tweet data.
And UDS converts it into the M2M Data Format for managing events, and then exports it.


UDS Has Built-in Sensor Templates
---------------------------------

Built-in Sensor Templates help to crawl data from a variety of data sources,
including web pages, Twitter, and the IEEE 1888 protocol.
You can define your own sensor templates if needed.


You Define *MySensor*
---------------------

You define your own unique sensor (*MySensor*) by customizing the built-in sensor templates.
*MySensor* is implemented in a following simple way.

*   Setting execution parameters of built-in sensor templates.

*   Implementing abstract methods of built-in sensor templates.


Core UDS SDK Development
------------------------

The User-Defined Sensor (UDS) SDK is an open-source project that is primarily being developed by
the National Institute of Information and Communications Technology's
Information Services Platform Laboratory (http://nict.go.jp/univ-com/isp/index.html).

