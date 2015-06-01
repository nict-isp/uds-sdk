# -*- coding: utf-8 -*-
import os

import uds.logging
from uds.sensors.twitter import TwitterSensor


class ExampleTwitterSensor(TwitterSensor):
    """Implementation example of HttpSensor.

    Advance preparation:
        Get parameters for Twitter Streaming API.

        * Consumer key
        * Consumer secret
        * Access token
        * Access secret
    """

    def __init__(self, project_home):
        super(ExampleTwitterSensor, self).__init__(project_home)

        # Set basic parameters
        self.sensor_name = "ExampleTwitterSensor"
        self.time_offset = '+00:00'

        # Set parameters for M2M Data
        self.m2m_info = {
            'formatVersion': '1.02',
            'srcContact': '',
            'createdContact': 'Test User<testuser@example.com>',
            'tag': '',
        }
        self.m2m_data_schema = [
            {'type': 'string', 'name': 'time'},
            {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'altitude', 'unit': 'm'},
            {'type': 'string', 'name': 'id_str'},
            {'type': 'string', 'name': 'tweet'},
        ]
        self.primary_keys = ['id_str']

        # Set parameters for filter
        self.filter_type = 'LIMITED_BUFFER_FILTER'

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

        # Set special parameters for TwitterSensor class.
        self.set_auth_params(
            consumer_key='YOUR_CONSUMER_KEY',
            consumer_secret='YOUR_CONSUMER_SECRET',
            access_key='YOUR_ACCESS_KEY',
            access_secret='YOUR_ACCESS_SECRET'
        )
        self.location_filter = [122.933611, 20.425277, 153.986388, 45.557777]

    def parse_data(self, data):
        # Prepare M2MData object
        m2m_data_list = []
        m2m_data = self.data_builder.create_m2m_data()
        m2m_datum = {}

        try:
            m2m_datum['tweet'] = data['text']
            m2m_datum['id_str'] = data['id_str']
            m2m_datum['time'] = data['created_at']

            if m2m_datum['geo'] is None:
                return {}
            m2m_datum['latitude'] = data['geo']['coordinates'][0]
            m2m_datum['longitude'] = data['geo']['coordinates'][1]
            m2m_datum['altitude'] = None
        except StandardError:
            uds.logging.error('[parse] Error.')
            return {}

        m2m_data.append(m2m_datum)
        m2m_data_list.append(m2m_data)

        return m2m_data_list


def get_sensor(project_home):
    return ExampleTwitterSensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()
