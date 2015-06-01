# -*- coding: utf-8 -*-
"""
uds.config.default_config
~~~~~~~~~~~~~~~~~~~~~~~~~

Default configuration values.

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import logging


#: Default value of :attr:`uds.sensors.base.Sensor.out_dir_path` .
OUT_DIR_PATH = '{PROJECT_HOME}/_out'

#: Default value of :attr:`uds.sensors.base.Sensor.log_dir_path` .
LOG_DIR_PATH = '{PROJECT_HOME}/_log'

#: Default value of :attr:`uds.sensors.base.Sensor.cache_dir_path` .
CACHE_DIR_PATH = '{PROJECT_HOME}/_cache'

#: Default value of :attr:`uds.sensors.base.Sensor.filter_type` .
FILTER_TYPE = 'time_order_filter'

#: Default value of :attr:`uds.sensors.base.Sensor.time_offset` .
TIME_OFFSET = '+00:00'

#: Default value of :attr:`uds.sensors.base.Sensor.store_type` .
STORE_TYPE = 'file'

#: Default value of :attr:`uds.sensors.base.Sensor.store_params` .
STORE_PARAMS = {
    'console': {},
    'file': {
        'dir_path': '{OUT_DIR_PATH}/m2m_data',
        'dir_file_max': 1000,
    },
    'mysql': {
        'user': None,
        'password': None,
        'host': None,
        'db': None,
        'table_name': None
    },
    'evwh': {
        'host': None,
        'port': None,
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
        'module_path':  None,
        'stub_module_enabled': True
    }
}

#: Default value of :attr:`uds.sensors.base.Sensor.time_record_enabled` .
TIME_RECORD_ENABLED = False

#: Default value of :attr:`uds.sensors.base.Sensor.log_enabled` .
LOG_FILE_ENABLED = True

#: Default value of :attr:`uds.sensors.base.Sensor.log_params` .
LOG_PARAMS = {
    'level': logging.INFO,
    'max_bytes': 1000*1000,
    'backup_count': 5
}

#: Default value of :attr:`uds.sensors.base.Sensor.ignore_confirmation` .
IGNORE_CONFIRMATION = False
