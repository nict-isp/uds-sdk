# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import csv
import re
import StringIO

import uds.logging
from uds.utils.string import try_parse_to_numeric
from uds.utils.string import try_parse_to_datetime
from uds.sensors.ieee1888 import IEEE1888Sensor


class ExampleIEEE1888Sensor(IEEE1888Sensor):
    """Implementation example of HttpSensor.

    *   Example data source 'http://ieee1888.example.com' is not exist in reality.
    """

    def __init__(self, project_home):
        super(ExampleIEEE1888Sensor, self).__init__(project_home)

        # Set basic parameters
        self.sensor_name = "ExampleIEEE1888Sensor"
        self.time_offset = '+09:00'

        # Set parameters for M2M Data
        self.m2m_info = {
            'formatVersion': '1.02',
            'srcContact': '',
            'createdContact': 'Test User<testuser@example.com>',
            'tag': '',
            'device': {
                'capability': {
                    'frequency': {
                        'type': 'hour',
                        'count': 1
                    }
                },
            }
        }
        self.m2m_data_schema = [
            {'type': 'string', 'name': 'time'},
            {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
            {'type': 'numeric', 'name': 'temperature', 'unit': '℃'}
        ]
        self.primary_keys = ['time', 'longitude', 'latitude']

        # Set parameters for store
        self.store_type = 'file'
        self.store_params = {
            'mysql': {
                'user': 'testuser',
                'password': 'testuser',
                'host': 'mysql-server.example.com',
                'db': 'UDSEventData'
            },
            'evwh': {
                'host': 'evwh-server.example.com',
                'port': 12345
            }
        }

        # Set special parameters for HttpSensor class.
        self.interval = 5
        self.wsdl_url = 'http://ieee1888.example.com/services/FIAPStorage?wsdl'

        # Set special parameters for ExampleIEEE1888Sensor class.
        self._pointList = []
        self._pointStartIndex = 0
        self._pointNextIndex = 0
        self._pointMaxKey = 50

    def create_query_keys(self):
        keys = []
        key1 = {
            '_attrName': 'time',
            '_id': 'http://ieee1888.example.com/weather/01001/airtmp',
            '_select': 'maximum'
        }
        keys.append(key1)

        return keys

    def parse_response(self, response):
        # Prepare M2MData object
        m2m_data_list = []

        try:
            response['header']['OK']
        except Exception as e:
            # Abort sensor
            uds.logging.critical('[parse] IEEE1888 response is NG')
            uds.logging.critical('[parse] > error_message=%s', e)
            sys.exit()

        for index, point in enumerate(response['body']['point']):
            m2m_data = self.data_builder.create_m2m_data()
            datum = {}

            # Set time and value
            for value in point['value']:
                datum['time'] = try_parse_to_datetime(str(value['_time']))
                datum['temperature'] = value['value']

            # Set location
            datum['latitude'] = 35.68
            datum['longitude'] = 139.76
            datum['altitude'] = None

            m2m_data.append(datum)
            m2m_data_list.append(m2m_data)

        return m2m_data_list


def get_sensor(project_home):
    return ExampleIEEE1888Sensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()