# -*- coding: utf-8 -*-
"""
uds.utils.benchmark
~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import os
import time
import csv


def get_time_recorder(time_record_enabled, log_dir_path, sensor_name, start_time):
    """

    :return:
    """
    if time_record_enabled:
        return TimeRecorder(log_dir_path, sensor_name, start_time)
    else:
        return NullTimeRecorder()


class TimeRecorder(object):
    
    def __init__(self, log_dir_path, sensor_name, start_time):
        self._dir_path = os.path.join(log_dir_path, 'time_record/')
        self._sensor_name = sensor_name
        self._start_time = start_time
        self._csv_writer = None
        self._file_name = None

    def write_header(self):
        # Prepare directory
        if not os.path.exists(self._dir_path):
            os.mkdir(self._dir_path)
        
        # Create file with sensor_name and start_time
        self._file_name = self._dir_path + self._sensor_name + self._start_time.strftime('_%Y%m%dT%H%M%S.csv')
        f = open(self._file_name, 'w')
        
        # Write header
        writer = csv.writer(f, dialect='excel-tab')
        writer.writerow([
            'interval_start_time',
            'fetch_time',
            'parse_time',
            'check_time',
            'filter_time',
            'store_time',
            'crawl_time',
        ])
        
        f.close()

    def write_record(self, time_record):
        f = open(self._file_name, 'a')
        writer = csv.writer(f, dialect='excel-tab')
        writer.writerow([
            time_record.interval_start_time,
            time_record.fetch_time,
            time_record.parse_time,
            time_record.check_time,
            time_record.filter_time,
            time_record.store_time,
            time_record.crawl_time,
        ])
        f.close()


class NullTimeRecorder(object):
    
    def __init__(self):
        pass

    def write_header(self):
        pass

    def write_record(self, time_record):
        pass
    

class TimeRecord(object):

    def __init__(self):
        self.interval_start_time = None
        self.fetch_time = 0.0
        self.parse_time = 0.0
        self.check_time = 0.0
        self.filter_time = 0.0
        self.store_time = 0.0
        self.crawl_time = 0.0


class Timer(object):
    
    def __init__(self):
        self._start = None
        self._end = None
        self._secs = 0.0
        self._msecs = 0.0
        self._is_working = False

    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()
    
    @property
    def secs(self):
        return self._secs

    @property
    def msecs(self):
        return self._msecs

    def start(self):
        assert not self._is_working, "Timer is already started."
        self._is_working = True
        
        self._start = time.time()
        return self

    def stop(self):
        assert self._is_working, "Timer is already stopped."
        self._is_working = False
        
        self._end = time.time()
        self._secs += self._end - self._start
        self._msecs + self._secs * 1000  # parse to millisecs


