# -*- coding: utf-8 -*-
import datetime
import unittest
from unittest import TestCase

from uds.utils.benchmark import get_time_recorder
from uds.utils.benchmark import TimeRecord


class TestBenchmark(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_str_to_loc_list(self):
        time_recorder = get_time_recorder(True, '../_log', 'TestBenchmark', datetime.datetime.now())
        time_recorder.write_header()

        time_record = TimeRecord()
        time_record.interval_start_time = datetime.datetime.now()
        time_record.fetch_time = 1
        time_record.parse_time = 2
        time_record.check_time = 3
        time_record.filter_time = 4
        time_record.store_time = 5
        time_record.crawl_time = 10
        time_recorder.write_record(time_record)
        time_recorder.write_record(time_record)
        time_recorder.write_record(time_record)
        time_recorder.write_record(time_record)


if __name__ == "__main__":
    unittest.main()