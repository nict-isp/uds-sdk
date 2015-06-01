# -*- coding: utf-8 -*-

TEST_M2M_DATA1 = {
    "primary": {
        "format_version": 1.02,
        "title": "SampleLocalFileSensor",
        "provenance": {
            "source": {
                "info": "C:\\_Git_\\uds-sdk\\uds\\sample\\2013-44-zensu.csv",
                "contact": ""
            },
            "create_by": {
                "contact": "ISP Guest User<ispguest@example.com>",
                "time": "2015-03-18 16:50:01.154000"
            }
        },
        "tag": "",
        "timezone": "+09:00",
        "security": "public",
        "id": "http://m2m.nict.go.jp/m2m_data/?id=SampleLocalFileSensor20150318165001154000"
    },
    "sensor_info": {
        "data_hash": "97da235b9ce7728ed52b8c71b09e7393",
        "data_link": {
            "uri": "C:\\_Git_\\uds-sdk/out/m2mdata\\SampleLocalFileSensor20150318164958/0000000000/M2MDataSampleLocalFileSensor20150318165001154000.json",
            "data_id": "SampleLocalFileSensor20150318165001154000"
        },
        "data_format": "json",
        "device_info": {
            "name": None,
            "serial_no": None,
            "capability": {
                "frequency": {
                    "count": 10,
                    "type": "minutes"
                }
            },
            "ownership": "NICT",
            "ipaddress": None,
            "id": None
        },
        "data_profile": "Weather",
        "data_size": 8550,
        "schema": [
            {
                "type": "numeric",
                "name": "ebora_report",
                "unit": "people"
            },
            {
                "type": "numeric",
                "name": "altitude",
                "unit": "m"
            },
            {
                "type": "numeric",
                "name": "longitude",
                "unit": "degree"
            },
            {
                "type": "numeric",
                "name": "ebora_total",
                "unit": "people"
            },
            {
                "type": "string",
                "name": "location"
            },
            {
                "type": "string",
                "name": "time"
            },
            {
                "type": "numeric",
                "name": "latitude",
                "unit": "degree"
            }
        ]
    },
    "data": {
        "values": [
            {
                "ebora_report": 0,
                "altitude": None,
                "longitude": 141.3468074,
                "ebora_total": 0,
                "location": "北海道",
                "time": "2013-10-28T00:00:00.000",
                "latitude": 43.0646147
            },
            {
                "ebora_report": 0,
                "altitude": None,
                "longitude": 140.7399984,
                "ebora_total": 0,
                "location": "青森県",
                "time": "2013-10-28T00:00:00.000",
                "latitude": 40.8243077
            },
            {
                "ebora_report": 0,
                "altitude": None,
                "longitude": 141.1526839,
                "ebora_total": 0,
                "location": "岩手県",
                "time": "2013-10-28T00:00:00.000",
                "latitude": 39.7036194
            }
        ],
        "data_id": "SampleLocalFileSensor20150318165001154000"
    }
}

TEST_M2M_DATA2 = {
    "primary": {
        "format_version": 1.02,
        "title": "ExampleCSVFileSensor01",
        "provenance": {
            "source": {
                "info": "localhost:2013-44-zensu.csv",
                "contact": ""
            },
            "create_by": {
                "contact": "Test User<testuser@example.com>",
                "time": "2015-03-18 17:47:44.856000"
            }
        },
        "tag": "",
        "timezone": "+09:00",
        "security": "public",
        "id": "http://m2m.nict.go.jp/m2m_data/?id=ExampleCSVFileSensor0120150318174744856000"
    },
    "sensor_info": {
        "data_hash": "912a10a91e5a792978c5872fbef4367d",
        "data_link": {
            "uri": "C:\\_Git_\\uds2-sdk/_out/evwh_error\\ExampleCSVFileSensor0120150318174743/0000000000/M2MDataExampleCSVFileSensor0120150318174744856000.json",
            "data_id": "ExampleCSVFileSensor0120150318174744856000"
        },
        "data_format": "json",
        "device_info": {
            "name": None,
            "serial_no": None,
            "capability": {
                "frequency": {
                    "count": 10,
                    "type": "minutes"
                }
            },
            "ownership": "NICT",
            "ipaddress": None,
            "id": None
        },
        "data_profile": "Weather",
        "data_size": 8511,
        "schema": [
            {
                "type": "numeric",
                "name": "ebora_report",
                "unit": "people"
            },
            {
                "type": "numeric",
                "name": "altitude",
                "unit": "degree"
            },
            {
                "type": "numeric",
                "name": "longitude",
                "unit": "degree"
            },
            {
                "type": "numeric",
                "name": "ebora_total",
                "unit": "people"
            },
            {
                "type": "string",
                "name": "location"
            },
            {
                "type": "string",
                "name": "time"
            },
            {
                "type": "numeric",
                "name": "latitude",
                "unit": "degree"
            }
        ]
    },
    "data": {
        "values": [
            {
                "ebora_report": 0,
                "altitude": None,
                "longitude": 127.6809317,
                "ebora_total": 0,
                "location": "沖縄県",
                "time": "2013-10-28T00:00:00.000",
                "latitude": 26.2124013
            },
            {
                "ebora_report": 0,
                "altitude": None,
                "longitude": 130.5579779,
                "ebora_total": 0,
                "location": "鹿児島県",
                "time": "2013-10-28T00:00:00.000",
                "latitude": 31.5601464
            },
            {
                "ebora_report": 0,
                "altitude": None,
                "longitude": 131.4238934,
                "ebora_total": 0,
                "location": "宮崎県",
                "time": "2013-10-28T00:00:00.000",
                "latitude": 31.9110956
            }
        ],
        "data_id": "ExampleCSVFileSensor0120150318174744856000"
    }

}