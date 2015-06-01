# -*- coding: utf-8 -*-
"""
uds.sensors.csvfile
~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import csv
from abc import abstractmethod

import uds.logging
from uds.sensors.base import Sensor
from uds.utils.crawling import Pacemaker


class CSVFileSensor(Sensor):
    """

    """

    def __init__(self, project_home):
        super(CSVFileSensor, self).__init__(project_home)
        self._interval = 0
        self._file_list = []
        self._pacemaker = None
        self._current_fp = None

    @property
    def interval(self):
        """Second-scale interval of reading one file.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: int
        """
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def file_list(self):
        """File list to read.

        :getter: Returns this parameter
        :type: list
        """
        return self._file_list

    def open(self):
        """Override of super class's method.
        """
        super(CSVFileSensor, self).open()
        self._pacemaker = Pacemaker(self.interval)

    def fetch(self):
        """Fetch csv file on the local machine.

        :return: CSVFileSource object including csv reader and file path.
        """
        self._pacemaker.wait()

        if len(self._file_list) == 0:
            uds.logging.info('[fetch] Stop crawl. File list to fetch is empty.')
            self.abort()
            return False

        file_path = self._file_list.pop(0)

        uds.logging.info('--- fetch start ----------------------------')
        uds.logging.info('[fetch] Open csv file. file_path=' + file_path)

        try:
            # Read csv file with 'rb' mode.
            fp = open(file_path, 'rb')
            rows = _read_csv(fp)
            fp.close()
        except Exception as e1:
            uds.logging.debug('[fetch] Failed to read csv file. Retry with other conditions')
            uds.logging.debug('[fetch] > file_path=%s', file_path)
            uds.logging.debug('[fetch] > error_message=%s', e1)
            try:
                # Read csv file with 'rU' mode.
                fp = open(file_path, 'rU')
                rows = _read_csv(fp)
                fp.close()
            except Exception as e2:
                uds.logging.error('[fetch] Failed to read csv file. file_path={0}'.format(file_path))
                raise e2

        uds.logging.info('[fetch] Close csv file.')

        source = CSVFileSource()
        source.rows = rows
        source.file_path = file_path
        return source

    def parse(self, source):
        """Override of super class's method.
        """
        m2m_data = self.parse_rows(source.rows, source.file_path)
        return m2m_data

    @abstractmethod
    def parse_rows(self, reader, file_path):
        """Parse reading csv rows to list of M2M Data.

        :param csv.reader reader: csv.reader object of python
        :param file_path: Reading file path.
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass


class CSVFileSource(object):
    """Fetch result object for CsvFileSensor.
    """
    def __init__(self):
        #: CSV rows
        self.rows = None
        #: CSV file path
        self.file_path = None


def _read_csv(fp):
    rows = []
    reader = csv.reader(fp)
    for index, row in enumerate(reader):
        # Parse to unicode
        row = [unicode(col, "Shift_JIS") for col in row]
        rows.append(row)
    return rows




        


