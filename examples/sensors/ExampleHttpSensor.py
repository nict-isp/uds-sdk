# -*- cod:ing: utf-8 -*-
import os
import re
from lxml import etree

import uds.logging
from uds.sensors.http import HttpSensor
from uds.utils.string import try_parse_to_numeric
from uds.utils.string import try_parse_to_datetime
from uds.utils.string import try_parse_to_string


class ExampleHttpSensor(HttpSensor):
    """Implementation example of HttpSensor.
    """

    def __init__(self, project_home):
        super(ExampleHttpSensor, self).__init__(project_home)

        # Set basic parameters
        self.sensor_name = "ExampleHttpSensor"
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
                        'type': 'seconds',
                        'count': 10
                    }
                }
            }
        }
        self.m2m_data_schema = [
            {'type': 'string', 'name': 'time'},
            {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
            {'type': 'numeric', 'name': 'rainfall', 'unit': 'mm'},
            {'type': 'string', 'name': 'city_name'},
            {'type': 'string', 'name': 'station_name'}
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
        self.interval = 10

        # Set special parameters for ExampleHttpSensor class.
        self._url_list = [
            'http://SAMPLE_DATA_LOCATION/sample-rainfall/pre1h/20140809T0900.html',
            'http://SAMPLE_DATA_LOCATION/sample-rainfall/pre1h/20140809T1000.html',
            'http://SAMPLE_DATA_LOCATION/sample-rainfall/pre1h/20140809T1100.html'
        ]

    def create_request(self):
        if len(self._url_list) == 0:
            self.abort()
            return None, None

        url = self._url_list.pop(0)
        return url, None

    def parse_content(self, content, url):
        # Prepare M2MData object
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()
        m2m_data.dict['primary']['provenance']['source']['info'] = url

        # Parse contents by use of lxml
        element = etree.HTML(content)

        # Parse data source time
        sensing_time = element.xpath('body/h1/text()')[0]
        match = re.match(u'(Hourly Precipitation Data )(.+)', sensing_time)
        if match:
            sensing_time = match.group(2)
            sensing_time = try_parse_to_datetime(sensing_time)
        else:
            uds.logging.error('[parse] Failed to parse time.')
            return m2m_data_list

        # Parse table rows
        tr_list = element.xpath('body/table/tbody/tr')

        for tr in tr_list:
            datum = {}

            datum['time'] = sensing_time
            datum['city_name'] = try_parse_to_string(
                tr.xpath('td[1]/text()')[0]
            )
            datum['station_name'] = try_parse_to_string(
                tr.xpath('td[2]/text()')[0]
            )
            datum['rainfall'] = try_parse_to_numeric(
                tr.xpath('td[3]/text()')[0]
            )

            # Geocode address to latitude/longitude
            geo_word = datum['city_name'] + ' ' + datum['station_name']
            loc_list = self.geocoder.str_to_loc_list(geo_word)
            if loc_list is False:
                # If failed, ignore the data
                uds.logging.warning('[parse] Can not Location Data.')
                continue
            else:
                datum["latitude"] = loc_list["latitude"]
                datum["longitude"] = loc_list["longitude"]
                datum["altitude"] = None

                m2m_data.append(datum)

        m2m_data_list.append(m2m_data)
        return m2m_data_list


def get_sensor(project_home):
    return ExampleHttpSensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()
