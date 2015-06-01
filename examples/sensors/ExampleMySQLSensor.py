# -*- coding: utf-8 -*-
import os
import datetime

from uds.sensors.mysql import MySQLSensor


class ExampleMySQLSensor(MySQLSensor):
    """Implementation example of HttpSensor

    *   Example data source 'mysql-server.example.com' is not exist in reality.
    """
    
    def __init__(self, project_home):
        super(ExampleMySQLSensor, self).__init__(project_home)
        
        # Set basic parameters
        self.sensor_name = "ExampleMySQLSensor"
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
                }
            }
        }
        self.m2m_data_schema = [
            {'type': 'string', 'name': 'time'},
            {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
            {'type': 'numeric', 'name': 'SO2', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'NO', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'NO2', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'SPM', 'unit': 'mg/m3'},
            {'type': 'numeric', 'name': 'PM2.5', 'unit': 'μg/m3'},
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
        self.interval = 3

        # Set special parameters for MySQLSensor class.
        self.mysql_fetch_params = {
            'user': 'testuser',
            'password': 'testuser',
            'host': 'mysql-server.example.com',
            'db': 'GeoSocialDatabase'
        }

        # Starting datetime for fetching data
        self._sensor_datetime = datetime.datetime(2013, 9, 30, 23, 0)

    def create_query(self):
        query = 'SELECT NIES_code, SO2, NO, NO2 '
        query += 'FROM japan_airpollution_data'
        query += 'WHERE log_datetime="2013-04-01T12:00:00"'

        # Abort next crawl
        self.abort()

        return query

    def parse_rows(self, rows):
        # Prepare M2M Data list
        m2m_data_list = []

        for row in rows:
            m2m_data = self.data_builder.create_m2m_data()
            datum = {}
            
            try:
                m2m_data.device_info['station_code'] = row[0]
                datum['latitude'] = 35.68
                datum['longitude'] = 139.76
                datum['time'] = str(self._sensor_datetime)
                datum['SO2'] = row[1]
                datum['NO'] = row[2]
                datum['NO2'] = row[3]
                datum['SPM'] = row[4]
                datum['PM2.5'] = row[5]

                m2m_data.append(datum)
                m2m_data_list.append(m2m_data)
            except StandardError:
                pass

        return m2m_data_list


def get_sensor(project_home):
    return ExampleMySQLSensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()