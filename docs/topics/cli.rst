Using the Command Line Tool
===========================

.. contents::
    :depth: 2

**API Reference**
    * :ref:`tools-api` » :class:`uds.tools.cli`

You can use the command line tool (the **uds** command) to easily create projects,
build sample sensors, run your own sensors, and more.


Viewing Version Information
---------------------------

Run **uds version** version to view your UDS SDK version.

::

    $ uds --version


Viewing Help
------------

Run **uds help** to view the uds command’s Help message.

::

    $ uds --help


Creating Projects
-----------------

Run uds **uds new-project** to create a UDS project.

*   Command syntax
        **uds new-project <project name>**

*   Sample invocation
        Create a new project named 'my-project'.
        ::

            $ uds new-project my-project


Creating Template Sensor Files
------------------------------

Run **uds new-sensor** to create template files for your own sensor.

*   Command syntax
        **uds new-sensor –t <template class name> <new sensor name>**

*   Sample invocation
        Create a new sensor named 'MyHttpSensor' that extends the HttpSensor template.
        ::

            $ uds new-sensor -t HttpSensor MyHttpSensor


Running *MySensor*
------------------

*   Command syntax
        **uds run <path to your sensor script>**

*   Sample invocation
        Run 'uds/impl/MyHttpSensor.py'.
        ::

            $ uds run udsimpl/sensors/MyHttpSensor.py
