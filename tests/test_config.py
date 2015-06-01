import unittest
from unittest import TestCase
import json
import os

import uds.logging
from uds.config import Config


class TestConfig(TestCase):

    def setUp(self):
        config_dir_path = os.path.join(os.path.dirname(__file__), '../uds/config')
        self._config = Config(config_dir_path)

    def test_from_pyfile(self):
        self._config.from_pyfile('default_config.py')

        print json.dumps(self._config, indent=2)

    def test_from_object(self):
        from uds.config import default_config
        self._config.from_object(default_config)

        print json.dumps(self._config, indent=2)

    def test_from_object_by_name(self):
        self._config.from_object('uds.config.default_config')

        print json.dumps(self._config, indent=2)


if __name__ == "__main__":
    unittest.main()