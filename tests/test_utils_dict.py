import unittest
from unittest import TestCase
import json

import uds.utils.dict


class TestUtilsDict(TestCase):

    STORE_PARAMS_0 = {
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
            'insert_timeout': None,
            'select_timeout': None,
            'primary_keys_enabled': False,
            'error_dir_path': '{OUT_DIR_PATH}/evwh_error'
        },
    }

    STORE_PARAMS_1 = {
        'console': {
            'aaa': 'absssss',
            'bbb': {
                'xxx': 1234
            }
        },
        'file': {
            'dir_file_max': 5000,
        },
        'mysql': {
            'host': 'mysql-server.example.com',
            'db': 'UserDefinedSensor_test',
        },
        'evwh': {
            'host': '192.168.1.1',
            'port': 11056,
        },
        'scn': {
            'scn_info': 'xxxxxxxxxx'
        }
    }

    def test_override_dict(self):
        result = uds.utils.dict.override_dict(TestUtilsDict.STORE_PARAMS_1, TestUtilsDict.STORE_PARAMS_0)
        print json.dumps(result, indent=2)
        print '--------------------------'
        result = uds.utils.dict.override_dict(TestUtilsDict.STORE_PARAMS_0, TestUtilsDict.STORE_PARAMS_1)
        print json.dumps(result, indent=2)


if __name__ == "__main__":
    unittest.main()