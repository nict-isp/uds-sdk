# -*- coding:utf-8 -*-
"""
uds.sensors.scn
~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import Queue
from abc import abstractmethod

import uds.logging
from uds.sensors.base import Sensor
from uds.scn import SCNApi


class SCNSensor(Sensor):
    """
    SCNSensor connects to and fetches data via Service-Controlled Networking (SCN).
    """

    def __init__(self, project_home):
        super(SCNSensor, self).__init__(project_home)
        self._scn_fetch_params = {
            'service_info': {
                'category': None,
                'type': None,
            },
            'module_path': None,
            'stub_mode_enabled': True
        }
        self._scn = None
        self._raw_data_queue = Queue.Queue()

    @property
    def scn_fetch_params(self):
        return self._scn_fetch_params

    @scn_fetch_params.setter
    def scn_fetch_params(self, value):
        self._scn_fetch_params = value

    def open(self):
        super(SCNSensor, self).open()

        self._scn = SCNApi(
            self.sensor_name,
            self.scn_fetch_params['service_info'],
            self.scn_fetch_params['module_path'],
            self.scn_fetch_params['stub_mode_enabled']
        )

        # Register sensor service to SCN.
        self._scn.create_service()

        # Register callback function
        self._scn.set_response(None, self.response)

    def response(self, data, service_link_id):
        """Callback function.
        """
        # Enqueue received data
        uds.logging.info('[fetch] Receive data from scn. service_link_id=%s, data=%s', service_link_id, data)

        self._raw_data_queue.put(data)

    def fetch(self):
        """Overridden method.

        :return: Received data from scn
        """
        raw_data = self._raw_data_queue.get()
        uds.logging.info('[fetch] Dequeue ----- queue num = %s', self._raw_data_queue.qsize())
        return raw_data

    def parse(self, source):
        """Overridden method.
        """
        return self.parse_data(source)

    @abstractmethod
    def parse_data(self, data):
        """Parse scn data to list of M2M Data.

        :param dict data: Received data from scn
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass

    def check(self, m2m_data_list):
        """Do nothing. (Overridden method)
        """
        return True

    def _commit(self, m2m_data_list):
        """Do nothing. (Overridden method)
        """
        return m2m_data_list

    def _show_confirmation(self):
        """
        Overridden method.
        """
        print 'Information Data'
        print '  SensorVersion : {0}'.format(Sensor.VERSION)
        print '  Title         : {0}'.format(self.sensor_name)
        print '  store         : {0}'.format(self.store_type.lower())
        print 'Check!!'
        print '  Start time  : {0}'.format(str(self.start_time))
        print '  Now   time  : {0}{1}'.format(uds.utils.datetime.get_now_time(self.time_offset), self.time_offset)
        if not self.ignore_confirmation:
            print raw_input('Please Enter')
        print
