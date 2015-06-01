# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
import json

import uds.logging
from uds.data.build import M2MDataBuilder
from uds.data.commit import M2MDataCommitter
from uds.data.check import M2MDataChecker


class TestM2MData(TestCase):

    def setUp(self):
        uds.logging.open_logging('./_log', 'TestM2MData')

    def tearDown(self):
        uds.logging.close_logging()

    def test_create_v101(self):
        builder = M2MDataBuilder()
        builder.title = 'TestM2MDataBuilder'
        builder.timezone = '+0900'
        builder.m2m_info = {
            'formatVersion': '1.01',
            'srcContact': '',
            'createdContact': 'ISP Guest User<ispguest@example.com>',
            'device': {
                'id': None,
                'ownership': None,
                'ipaddress': None,
                'name': None,
                'serial_no': None,
            },
            'capability': {
                'frequency': {
                    'type': 'hour',
                    'count': 1
                },
            },
            'security': 'public',
            'tag': '',
        }
        builder.m2m_data_schema = [
            {'type': 'numeric', 'name': 'SO2', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'NO', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'NO2', 'unit': 'ppm'},
            {'type': 'datetime', 'name': 'time'}
        ]
        m2m_data = builder.create_m2m_data()
        print json.dumps(m2m_data.dict, indent=2)

    def test_create_v102(self):
        builder = M2MDataBuilder()
        builder.title = 'TestM2MDataBuilder'
        builder.timezone = '+0900'
        builder.m2m_info = {
            'formatVersion': '1.02',
            'srcContact': '',
            'createdContact': 'ISP Guest User<ispguest@example.com>',
            'device': {
                'id': None,
                'ownership': None,
                'ipaddress': None,
                'name': None,
                'serial_no': None,
            },
            'capability': {
                'frequency': {
                    'type': 'hour',
                    'count': 1
                },
            },
            'security': 'public',
            'tag': '',
        }
        builder.m2m_data_schema = [
            {'type': 'datetime', 'name': 'time'},
            {'type': 'numeric', 'name': 'longitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'latitude', 'unit': 'degree'},
            {'type': 'numeric', 'name': 'SO2', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'NO', 'unit': 'ppm'},
            {'type': 'numeric', 'name': 'NO2', 'unit': 'ppm'},
        ]
        builder.primary_keys = ['time', 'longitude', 'latitude']
        m2m_data = builder.create_m2m_data()
        # print json.dumps(m2m_data.dict, indent=2)

        m2m_data.append({'time': '2015-02-16T00:00:00',
                         'longitude': 128,
                         'latitude': 38,
                         'SO2': 0.1,
                         'NO': 0.2,
                         'NO2': 0.3})

        m2m_data.append({'time': '2015-02-16T01:00:00',
                         'longitude': 150,
                         'latitude': 50,
                         'SO2': 1.1,
                         'NO': 1.2,
                         'NO2': 1.3})

        m2m_data.append({'time': '2015-02-16T02:00:00',
                         'longitude': 128,
                         'latitude': 38,
                         'SO2': 2.1,
                         'NO': 2.2,
                         'NO2': 2.3})

        # print m2m_data[0]
        # print m2m_data[1]
        # print m2m_data[2]

        return m2m_data

    def test_commit_v102(self):
        m2m_data = self.test_create_v102()
        committer = M2MDataCommitter()
        m2m_data = committer.process(m2m_data)

        # print json.dumps(m2m_data.dict, indent=2)

        # Check pk_values
        # pk_values = m2m_data.get_pk_values(m2m_data[0])
        # print pk_values

        return m2m_data

    def test_check_v102(self):
        m2m_data = self.test_commit_v102()
        checker = M2MDataChecker()
        is_ok = checker.process(m2m_data)

        # Check properties
        pk_values = m2m_data.get_pk_values(m2m_data[0])
        print pk_values
        print m2m_data.data_id
        print m2m_data.min_time
        print m2m_data.max_time
        print m2m_data.south
        print m2m_data.north
        print m2m_data.west
        print m2m_data.east

        print is_ok


if __name__ == "__main__":
    unittest.main()
