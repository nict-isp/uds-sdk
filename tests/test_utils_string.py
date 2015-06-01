import unittest
from unittest import TestCase


import uds.utils.string as util


class TestStrings(TestCase):

    def test_try_parse_to_numeric(self):
        numeric_value = util.try_parse_to_numeric('12.24')
        assert isinstance(numeric_value, float)
        print numeric_value

        numeric_value = util.try_parse_to_numeric('ABC')
        assert numeric_value is None
        print numeric_value

    def test_try_parse_to_datetime(self):
        datetime_string = util.try_parse_to_datetime('2014-12-10T01:01:01+0900')
        assert isinstance(datetime_string, str)
        print datetime_string

        datetime_string = util.try_parse_to_datetime('2014-12-10T01:01:01')
        assert isinstance(datetime_string, str)
        print datetime_string

        datetime_string = util.try_parse_to_datetime('2014-12-10')
        assert isinstance(datetime_string, str)
        print datetime_string

        datetime_string = util.try_parse_to_datetime('2014')
        assert isinstance(datetime_string, str)
        print datetime_string


if __name__ == "__main__":
    unittest.main()