import unittest
from unittest import TestCase

import uds.logging


class TestLogging(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_info(self):
        uds.logging.info('this is info message. args1=%s args2=%s', 'Xxxxxx', 'Yyyyy')

    def test_warning(self):
        uds.logging.warning('this is warning message.')

    def test_error(self):
        uds.logging.error('this is error message.')

    def test_critical(self):
        uds.logging.critical('this is critical message.')

    def _test_write_many(self):
        for i in range(1000):
            uds.logging.info('Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.')


if __name__ == "__main__":
    unittest.main()
