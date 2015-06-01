# -*- coding: utf-8 -*-
"""
uds.sensors.base
~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""

import os
import datetime
from abc import ABCMeta
from abc import abstractmethod

import uds.logging
import uds.utils.datetime
import uds.utils.dict
from uds.utils.benchmark import get_time_recorder
from uds.utils.benchmark import TimeRecord
from uds.utils.benchmark import Timer
from uds.config import Config
from uds.config import default_config
from uds.utils import benchmark
from uds.utils.geocoders import Geocoder
from uds.data.build import M2MDataBuilder
from uds.data.commit import M2MDataCommitter
from uds.data.check import M2MDataChecker
import uds.filters
import uds.stores


class Sensor():
    """

    """

    __metaclass__ = ABCMeta
    VERSION = '2.0.0'
    PROJECT_CONFIG_FILE = 'project_config.py'

    def __init__(self, project_home):
        assert isinstance(project_home, str)

        # Start time of sensor.
        self._start_time = datetime.datetime.now()

        # Execution Parameters
        self._project_home = project_home
        self._config = self._make_config()
        self._sensor_name = None
        self._m2m_info = {}
        self._m2m_data_schema = []
        self._primary_keys = []
        self._store_table_name = None

        # Subsidiary Objects
        self._time_recorder = None
        self._data_builder = None
        self._geocoder = Geocoder(self.cache_dir_path)
        self._data_committer = M2MDataCommitter()
        self._data_checker = M2MDataChecker()
        self._filter = None
        self._store = None

        self._abort_requested = False

    def _make_config(self):
        config = Config(self.config_dir_path)

        # Load sdk default config
        config.from_object(default_config)

        # load user project config
        project_config_path = os.path.join(self.config_dir_path, Sensor.PROJECT_CONFIG_FILE)
        if os.path.exists(project_config_path):
            config.from_pyfile(Sensor.PROJECT_CONFIG_FILE)

        return config

    @property
    def start_time(self):
        """ Starting datetime of executing sensor.

        :getter: Returns this parameter
        :type: :class:`datetime`
        """
        return self._start_time

    @property
    def project_home(self):
        """Directory path of Project Home to execute sensor.

        :getter: Returns this parameter
        :type: :class:`str`
        """
        return self._project_home

    @property
    def config_dir_path(self):
        """Directory path for configuration.

        :getter: Returns this parameter
        :type: :class:`str`
        """
        return os.path.join(self._project_home, 'conf')

    @property
    def log_dir_path(self):
        """Directory path for writing log.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._config['LOG_DIR_PATH'].replace('{PROJECT_HOME}', self.project_home)

    @log_dir_path.setter
    def log_dir_path(self, value):
        self._config['LOG_DIR_PATH'] = value

    @property
    def out_dir_path(self):
        """Directory path for storing data to local.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._config['OUT_DIR_PATH'].replace('{PROJECT_HOME}', self.project_home)

    @out_dir_path.setter
    def out_dir_path(self, value):
        self._config['OUT_DIR_PATH'] = value

    @property
    def cache_dir_path(self):
        """Directory path for caching fetched data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._config['CACHE_DIR_PATH'].replace('{PROJECT_HOME}', self.project_home)

    @cache_dir_path.setter
    def cache_dir_path(self, value):
        self._config['CACHE_DIR_PATH'] = value

    @property
    def sensor_name(self):
        """Sensor name. This parameter is used as follows.

        - Title of M2M Data
        - File output directory name

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._sensor_name

    @sensor_name.setter
    def sensor_name(self, value):
        self._sensor_name = value

    @property
    def time_offset(self):
        """Timezone of M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return uds.utils.datetime.normalize_timezone(self._config['TIME_OFFSET'])

    @time_offset.setter
    def time_offset(self, value):
        self._config['TIME_OFFSET'] = value

    @property
    def m2m_info(self):
        """Default information values of metadata part of M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`dict`
        """
        return self._m2m_info

    @m2m_info.setter
    def m2m_info(self, value):
        self._m2m_info = value

    @property
    def m2m_data_schema(self):
        """Data schema definition of data part of M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`dict`
        """
        return self._m2m_data_schema

    @m2m_data_schema.setter
    def m2m_data_schema(self, value):
        self._m2m_data_schema = value

    @property
    def primary_keys(self):
        """Primary keys of M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`list`
        """
        return self._primary_keys

    @primary_keys.setter
    def primary_keys(self, value):
        self._primary_keys = value

    @property
    def config(self):
        """Configuration object.

        :getter: Returns this parameter
        :type: :class:`uds.config.Config`
        """
        return self._config

    @property
    def filter_type(self):
        """Type of filter to apply.
        Sets one of following values.

            *   'time_order_filter' --
            *   'limited_buffer_filter' --
            *   'no_filter' -- Use no filter.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._config['FILTER_TYPE']

    @filter_type.setter
    def filter_type(self, value):
        self._config['FILTER_TYPE'] = value

    @property
    def store_type(self):
        """Type of output location.
        Sets one of following values.

            *   'console' -- Use console output.
            *   'file' -- Use local file output.
            *   'mysql' -- Use MySQL output.
            *   'evwh' -- Use Event Warehouse output.
            *   'scn' -- Use SCN output.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._config['STORE_TYPE']

    @store_type.setter
    def store_type(self, value):
        self._config['STORE_TYPE'] = value

    @property
    def store_params(self):
        """Information for storing data.

        *   'console':

            No parameters.

        *   'file':

            *   'dir_path' -- Directory path for storing M2M Data file.
            *   'dir_file_max' -- Max file number in same directory.

        *   'mysql':

            *   'user' --
            *   'password' --
            *   'host' --
            *   'db' --
            *   'table_name' --

        *   'evwh':

            *   'host' --
            *   'port' --
            *   'insert_timeout' --
            *   'select_timeout' --
            *   'table_name' --
            *   'insert_timeout' -- Timeout for EventWarehouse connections in INSERT query.
            *   'select_timeout' -- Timeout for EventWarehouse connections in SELECT query.
            *   'primary_keys_enabled' -- In INSERT query, use primary key constraints
                by use of Event Warehouse's Conditional Insert.

        *   'scn':

            *   'service_info':

                *   'category' --
                *   'type' --

            *   'module_path' --
            *   'stub_module_enabled' --

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`dict`
        """
        return self._config['STORE_PARAMS']

    @store_params.setter
    def store_params(self, value):
        self._config['STORE_PARAMS'] = uds.utils.dict.override_dict(value, self._config['STORE_PARAMS'])

    @property
    def time_record_enabled(self):
        """enable/disable processing time of sensor.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`bool`
        """
        return self._config['TIME_RECORD_ENABLED']

    @time_record_enabled.setter
    def time_record_enabled(self, value):
        self._config['TIME_RECORD_ENABLED'] = value

    @property
    def log_file_enabled(self):
        """enable/disable writing log to file.

        * 'level':
        * 'max_bytes': Max bytes for log file.
        * 'backup_count': Backup count for log file.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`bool`
        """
        return self._config['LOG_FILE_ENABLED']

    @log_file_enabled.setter
    def log_file_enabled(self, value):
        self._config['LOG_FILE_ENABLED'] = value

    @property
    def log_params(self):
        """Configuration parameters for logging

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`dict`
        """
        return self._config['LOG_PARAMS']

    @log_params.setter
    def log_params(self, value):
        self._config['LOG_PARAMS'] = uds.utils.dict.override_dict(value, self._config['LOG_PARAMS'])

    @property
    def ignore_confirmation(self):
        """enable/disable showing confirmation when execution sensor.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`bool`
        """
        return self._config['IGNORE_CONFIRMATION']

    @ignore_confirmation.setter
    def ignore_confirmation(self, value):
        self._config['IGNORE_CONFIRMATION'] = value

    @property
    def data_builder(self):
        """Utility to build M2M Data object.

        :getter: Returns this parameter
        :type: :class:`uds.data.build.M2MDataBuilder`
        """
        return self._data_builder

    @property
    def geocoder(self):
        """Utility of geocoding.

        :getter: Returns this parameter
        :type: :class:`uds.utils.geocoders.Geocoder`
        """
        return self._geocoder

    def run(self):
        """Run sensor.

        :return: None
        """

        # Check execution parameters
        if not check_params(self):
            print '[check_params] Parameter check result is false. Abort sensor!'
            return

        # ※ timeOffsetのフォーマット修正も同時に行う。
        self._show_confirmation()

        self.open()

        while not self._abort_requested:
            # Begin record time
            time_record = TimeRecord()
            time_record.interval_start_time = datetime.datetime.now()
            timer0 = Timer()
            timer0.start()

            # Before cycle
            self.before_cycle()

            # Fetch
            with Timer() as timer1:
                source = self.fetch()
            time_record.fetch_time = timer1.secs

            if not source:
                self._time_recorder.write_record(time_record)
                uds.logging.info('[fetch] Fetch result is none. Continue to next crawling cycle.')
                continue

            # Parse
            with Timer() as timer2:
                m2m_data_list = self.parse(source)
            time_record.parse_time = timer2.secs

            if len(m2m_data_list) == 0:
                uds.logging.info('[parse] Parse result is none. Continue to next crawling cycle.')
                continue

            # Commit
            m2m_data_list = self._commit(m2m_data_list)

            # Check
            with Timer() as timer3:
                check_result = self.check(m2m_data_list)
            time_record.check_time = timer3.secs

            if check_result is False:
                uds.logging.error("[check] Parsed m2m_data_list is invalid. Continue to next crawling cycle.")
                continue

            # Filter
            with Timer() as timer4:
                m2m_data_list = self.filter(m2m_data_list)
            time_record.filter_time = timer4.secs

            if len(m2m_data_list) == 0:
                uds.logging.info("[filter] Filtered m2m_data_list is none. Continue to next crawling cycle.")
                continue

            # Store
            with Timer() as timer5:
                self.store(m2m_data_list)
            time_record.store_time = timer5.secs

            # After cycle
            self.after_cycle()

            # End record time
            timer0.stop()
            time_record.crawl_time = timer0.secs
            self._time_recorder.write_record(time_record)

        self.close()

    def abort(self):
        """Abort sensor.

        :return: None
        """
        self._abort_requested = True

    def _show_confirmation(self):
        if 'createdContact' in self.m2m_info:
            created_contact = self.m2m_info['createdContact']
        else:
            created_contact = 'Undefined'

        print 'Information Data'
        print '  SensorVersion : {0}'.format(Sensor.VERSION)
        print '  Title         : {0}'.format(self.sensor_name)
        print '  createdContact: {0}'.format(created_contact)
        print '  store         : {0}'.format(self.store_type.lower())
        print 'Check!!'
        print '  Start time  : {0}'.format(str(self.start_time))
        print '  Now   time  : {0}{1}'.format(uds.utils.datetime.get_now_time(self.time_offset), self.time_offset)
        if not self.ignore_confirmation:
            print raw_input('Please Enter')
        print

    def open(self):
        """Process before starting crawling cycles.

        :return: None.
        """
        # Update config
        self._resolve_params()

        # Setup uds.logging
        uds.logging.configure(self.sensor_name, self.log_dir_path, self.log_file_enabled, self.log_params)

        # Setup time_recorder
        self._time_recorder = get_time_recorder(
            self.time_record_enabled,
            self.log_dir_path,
            self.sensor_name,
            self.start_time
        )
        self._time_recorder.write_header()

        # Setup data_builder
        self._data_builder = M2MDataBuilder()
        self._data_builder.title = self.sensor_name
        self._data_builder.timezone = self.time_offset
        self._data_builder.m2m_info = self.m2m_info
        self._data_builder.m2m_data_schema = self.m2m_data_schema
        self._data_builder.primary_keys = self.primary_keys

        # Setup filter
        self._filter = uds.filters.get_filter(
            self.filter_type, self.store_type, self.store_params, self.sensor_name, self.start_time)
        self._filter.open()

        # Setup store
        self._store = uds.stores.get_store(self.store_type, self.store_params, self.sensor_name, self.start_time)
        self._store.open()

    def _resolve_params(self):
        if 'file' in self.store_params:
            self.store_params['file']['dir_path'] =\
                self._resolve_path(self.store_params['file']['dir_path'])

        if 'evwh' in self.store_params:
            if self.store_params['evwh']['table_name'] is None:
                self.store_params['evwh']['table_name'] = self.sensor_name

            self.store_params['evwh']['error_dir_path'] = self._resolve_path(
                self.store_params['evwh']['error_dir_path'])

        if 'mysql' in self.store_params:
            if self.store_params['mysql']['table_name'] is None:
                self.store_params['mysql']['table_name'] = self.sensor_name

        if 'scn' in self.store_params:
            self.store_params['scn']['module_path'] =\
                self._resolve_path(self.store_params['scn']['module_path'])

    def _resolve_path(self, path):
        if path is None:
            return
        path = path.replace('{PROJECT_HOME}', self.project_home)
        path = path.replace('{OUT_DIR_PATH}', self.out_dir_path)
        path = path.replace('{LOG_DIR_PATH}', self.log_dir_path)
        path = path.replace('{CACHE_DIR_PATH}', self.cache_dir_path)
        path = path.replace('{CONFIG_DIR_PATH}', self.config_dir_path)
        return path

    def close(self):
        """Process after starting crawling cycles.

        :return: None.
        """
        self._filter.close()
        self._store.close()

    def before_cycle(self):
        """Process before starting a single crawling cycle.
        :return: None.
        """
        pass

    def after_cycle(self):
        """Process after starting a single crawling cycle.
        :return: None.
        """
        pass

    @abstractmethod
    def fetch(self):
        """Fetch contents from data source.

        :return: Fetched object.
        :rtype: :class:`object`
        """
        pass

    @abstractmethod
    def parse(self, source):
        """Parse fetched contents to list of M2M Data.

        :param source: Fetched source object
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass

    def _commit(self, m2m_data_list):
        """Commit list of M2M Data.

        :param m2m_data_list: list of M2M Data
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        committed_list = []
        for m2m_data in m2m_data_list:
            committed = self._data_committer.process(m2m_data)
            committed_list.append(committed)
        return committed_list

    def check(self, m2m_data_list):
        """Check M2M Data.

        :param m2m_data_list: list of M2M Data
        :return: Target M2M Data list is valid or not.
        :rtype: :class:`bool`
        """
        for m2m_data in m2m_data_list:
            if self._data_checker.process(m2m_data) is False:
                return False
        return True

    def filter(self, m2m_data_list):
        """Delete overlap data in M2M Data list.

        :param m2m_data_list: list of M2M Data
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        return self._filter.filter(m2m_data_list)

    def store(self, m2m_data_list):
        """Store M2M Data to selected destination.

        :param m2m_data_list: List of M2M Data
        :return: None
        """

        self._store.store(m2m_data_list)


def check_params(sensor):
    result = True

    # Check sensor_name
    if sensor.sensor_name == '':
        print "[check_params] Parameter 'title' is not set."
        result = False

    # Check store_type
    if check_store_params(
        sensor.filter_type,
        sensor.store_type,
        sensor.primary_keys,
        sensor.store_params
    )is False:
        result = False

    return result


def check_store_params(filter_type, store_type, primary_keys, store_params):
    result = True

    # Check store_type
    if store_type.lower() not in ['console', 'file', 'mysql', 'evwh', 'scn']:
        print "[check_params] Parameter 'store_type' is invalid. store_type=%s" % store_type
        result = False

    # Check primary_keys with filter_type
    if store_type == 'evwh':
        if filter_type.lower() == 'no_filter':
            if store_params['evwh']['primary_keys_enabled'] is False:
                if len(primary_keys) != 0:
                    result = False
        elif filter_type.lower() == 'time_order_filter':
            if not ("time" in primary_keys and "longitude" in primary_keys and "latitude" in primary_keys):
                result = False
        elif filter_type.lower() == 'limited_buffer_filter':
            if len(primary_keys) == 0:
                result = False

    if result is False:
        print '[check_params] Parameter primary_keys is invalid for filter and store conditions.'
        print '[check_params] > filter_type=%s' % filter_type
        print '[check_params] > store_type=%s' % store_type
        print '[check_params] > evwh_primary_key_enabled=%s' % store_params['evwh']['primary_keys_enabled']
        print '[check_params] > primary_keys=%s' % primary_keys

    return result


