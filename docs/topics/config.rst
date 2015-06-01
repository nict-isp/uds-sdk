Using Configuration
===================

.. contents::
    :depth: 2

**API Reference**
    * :ref:`config-api`
    * :ref:`sensors-api` » :attr:`uds.sensors.base.Sensor.config`

Several of the :class:`~uds.sensors.base.Sensor` class's runtime parameters
can use default settings shared by the entire project.
These values are configured in your project settings file
and will be loaded when your sensor is initialized.
You can also add your own unique settings to the project settings file.

Accessing Settings
------------------

Use the :attr:`~uds.sensors.base.Sensor.config` property to directly access settings
from your sensor class, specifying their names as dictionary keys.

.. code-block:: python

    class MySensor(Sensor):
        def __init__(self):
            # * * * snip * * *
            self.config['STORE_TYPE'] = 'mysql'
            # * * * snip * * *

There is also a Sensor class property for each of these settings.

.. code-block:: python

    class MySensor(Sensor):
        def __init__(self):
            # * * * snip * * *
            self.store_type = 'mysql'
            # * * * snip * * *

Project Configuration File
--------------------------

The Project Configuration file is saved in the following directory.

    **<PROJECT_HOME>/_conf/project_conf.py**

As shown below, the settings file contains Python variable assignments.

.. code-block:: python

    # -*- coding: utf-8 -*-
    import logging

    FILTER_TYPE = 'time_order_filter'
    TIME_OFFSET = '+00:00'
    STORE_TYPE = 'file'
    STORE_PARAMS = {
        'console': {},
        'file': {
            'dir_path': '{OUT_DIR_PATH}/m2m_data',
            'dir_file_max': 1000,
        },
        'mysql': {
            'user': 'testuser',
            'password': 'testuser',
            'host': 'mysql-server.example.com',
            'db': 'UDSEventData',
            'table_name': None
        },
        'evwh': {
            'host': 'evwh-server.example.com',
            'port': 12345,
            'table_name': None,
            'insert_timeout': 2,
            'select_timeout': 2,
            'primary_keys_enabled': False,
            'error_dir_path': '{OUT_DIR_PATH}/evwh_error'
        },
        'scn': {
            'service_info': {
                'category': None,
                'type': None,
            },
            'module_path': None,
            'stub_module_enabled': True
        }
    }
    TIME_RECORD_ENABLED = False
    LOG_FILE_ENABLED = True
    LOG_PARAMS = {
        'level': logging.INFO,
        'max_bytes': 1000 * 1000,
        'backup_count': 5
    }
    IGNORE_CONFIRMATION = False

Load Order
----------

Configurations are loaded—and overwritten—in the following order when your sensor is initialized.

#.  The constants defined in :attr:`uds.config.default_config` are loaded.

#.  Existing settings are overwritten by shared project settings loaded from
    **<PROJECT_HOME>/_conf/project_conf.py**

#.  Existing settings are overwritten by the parameters set in the Sensor class's
    :attr:`~uds.sensors.base.Sensor.config` property.



Built-In Default Configurations
-------------------------------

The following default settings are built into the SDK.

* :attr:`uds.config.default_config`