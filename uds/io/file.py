# -*- coding: utf-8 -*-
"""
uds.io.file
~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import os
from uds.io.base import M2MDataDao


class FileDao(M2MDataDao):
    """

    """

    def __init__(self, sensor_name, start_time, dir_path, dir_file_max):
        super(FileDao, self).__init__()
        self._sensor_name = sensor_name
        self._start_time = start_time
        self._dir_path = dir_path
        self._dir_file_max = dir_file_max
        self._dir_num = 0  # Directory number
        self._dir_file_num = 0  # File number contained in the directory.

    def reconnect(self):
        pass

    def select_last(self, key_data):
        return None

    def insert(self, m2m_data):
        """

        :param m2m_data:
        :return:
        """
        # Create output directory
        if not os.path.exists(self._dir_path):
            os.mkdir(self._dir_path)

        # Create output directory for a sensor. dir_name=[title][start-up datetime]
        dir_name = os.path.join(
            self._dir_path, self._sensor_name + self._start_time.strftime('%Y%m%d%H%M%S') + '/')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

            # Create sub directory
            dir_name = dir_name + '%010d' % self._dir_num + '/'
            os.mkdir(dir_name)

        # Decide sub directory number, then create sub directory.
        elif self._dir_file_num > self._dir_file_max:
            self._dir_num += 1
            dir_name = dir_name + '%010d' % self._dir_num + '/'
            os.mkdir(dir_name)

            self._dir_file_num = 0

        else:
            dir_name = dir_name + '%010d' % self._dir_num + '/'

        # Commit data_link uri of metadata.
        file_name = dir_name + 'M2MData' + m2m_data.dict['sensor_info']['data_link']['data_id'] + '.json'
        m2m_data.dict['sensor_info']['data_link']['uri'] = file_name

        # Write data part
        self._write_data_part(file_name, m2m_data)

        # Write metadata part
        file_name = dir_name + 'M2MmetaData' + m2m_data.dict['sensor_info']['data_link']['data_id'] + '.json'
        self._write_metadata_part(file_name, m2m_data)

        self._dir_file_num += 1

    @staticmethod
    def _write_data_part(file_path, m2m_data):
        data_str = str(m2m_data.data_json)
        fp = open(file_path, 'w')
        fp.write(data_str)
        fp.close()

    @staticmethod
    def _write_metadata_part(file_path, m2m_data):
        metadata_str = str(m2m_data.metadata_json)
        fp = open(file_path, 'w')
        fp.write(metadata_str)
        fp.close()
