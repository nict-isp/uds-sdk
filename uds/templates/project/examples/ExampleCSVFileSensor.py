# -*- coding: utf-8 -*-
import os
import re

import uds.logging
from uds.utils.string import try_parse_to_numeric
from uds.utils.string import try_parse_to_datetime
from uds.utils.string import try_parse_to_string
from uds.sensors.csvfile import CSVFileSensor


class ExampleCSVFileSensor(CSVFileSensor):
    """Implementation example of CSVFileSensor.
    """
    
    def __init__(self, project_home):
        CSVFileSensor.__init__(self, project_home)

        # Set basic parameters
        self.sensor_name = "ExampleCSVFileSensor01"
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

        # Set Second-scale interval of crawling cycle.
        self.interval = 10

        # Set file list to read.
        dir_path = os.path.abspath(os.path.dirname(__file__))
        self.file_list.append(os.path.join(dir_path, '../sample_rainfall/pre1h/20140809T0900.csv'))
        self.file_list.append(os.path.join(dir_path, '../sample_rainfall/pre1h/20140809T1000.csv'))
        self.file_list.append(os.path.join(dir_path, '../sample_rainfall/pre1h/20140809T1100.csv'))

    def parse_rows(self, rows, file_path):
        # Prepare M2MData object
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()
        m2m_data.dict['primary']['provenance']['source']['info'] = file_path

        # Parse data source time
        match = re.search(u'(\d\d\d\d)(\d\d)(\d\d)T(\d\d)(\d\d)', file_path)
        if match:
            yyyy = match.group(1)
            mm = match.group(2)
            dd = match.group(3)
            hh = match.group(4)
            MM = match.group(5)
            sensing_time = '{yyyy}-{mm}-{dd}T{hh}:{MM}'.format(yyyy=yyyy, mm=mm, dd=dd, hh=hh, MM=MM)
            sensing_time = try_parse_to_datetime(sensing_time)
        else:
            uds.logging.error('[parse] Failed to parse time.')
            return m2m_data_list

        for idx, row in enumerate(rows):
            # Skip header
            if idx == 0:
                continue

            datum = {}

            datum['time'] = sensing_time
            datum['city_name'] = try_parse_to_string(
                row[0]
            )
            datum['station_name'] = try_parse_to_string(
                row[1]
            )
            datum['rainfall'] = try_parse_to_numeric(
                row[2]
            )

            # Geocode address to latitude/longitude
            geo_word = datum['city_name'] + ', ' + datum['station_name']
            geo_word = datum['station_name'] + ', ' + datum['city_name']
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
    return ExampleCSVFileSensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()
