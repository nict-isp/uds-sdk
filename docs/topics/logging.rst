Using Logger
============

.. contents::
    :depth: 2

**API Reference**
    * :ref:`logging-api`

UDS add runtime information or error messages to log output in its execution.
You can also add your own messages to the log output.

Adding Messages to Log Output
-----------------------------

Use the :attr:`uds.logging` module to add messages to the log.

.. code-block:: python

    import uds.logging

    class MySensor(Sensor):
        def __init__(self):...

        def fetch()...

        def parse():
            # * * * snip * * *
            uds.logging.info('This is info message.')
            uds.logging.warning('This is warning message.')
            uds.logging.error('This is error message.')
            uds.logging.critical('This is critical message.')
            # * * * snip * * *

Messages have four log levels: “INFO,” “WARNING,” “ERROR,” and “CRITICAL.”
These are used with the same semantics as the corresponding log levels
in the Python logging module (https://docs.python.org/2/library/logging.html).

Log Directory and Rotation
--------------------------

Log files are saved to the following directory and are also rotated.

    **<PROJECT_HOME>/_log/<SENSOR_NAME>.log**

Sample log directory:

::

    project-name
        |─ _cache
        |─ _log
        |   |─ MySensor.log
        |   |─ MySensor.1.log
        |   |─ MySensor.2.log
        |   |─ MySensor.3.log
        |   |─ MySensor.4.log
        |   └─ MySenso.5.log
        |─ _out
        |─ conf
        |─ examples
        └─ udsimpl


