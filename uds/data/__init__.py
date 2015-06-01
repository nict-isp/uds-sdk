# -*- coding: utf-8 -*-
"""
uds.data
~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""

from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

import json
import dateutil.parser


class M2MDataVisitor(object):
    """
    Visitor interface for M2MData class.
    """

    __metaclass__ = ABCMeta

    def process(self, m2m_data):
        """Do something process about the M2MData object.

        :param m2m_data: M2MData object
        :return: Result of processing
        :rtype: :class:`object`
        """
        return m2m_data.accept(self)

    @abstractmethod
    def visit_v101(self, m2m_data):
        """Do something process about the v1.01 M2MData object.

        :param M2MDataV101 m2m_data:
        :return: Result of processing
        :rtype: :class:`object`
        """
        pass

    @abstractmethod
    def visit_v102(self, m2m_data):
        """Do something process about the v1.02 M2MData object.

        :param M2MDataV101 m2m_data:
        :return: Result of processing
        :rtype: :class:`object`
        """
        pass


class M2MData(object):
    """M2MData object keeps values defined in terms of M2M Data Format.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self._dict = None
        self._is_commit = False
        self._primary_keys = {}
        self._info_summary = None

    @abstractmethod
    def __getitem__(self, i):
        pass

    @abstractproperty
    def version(self):
        """Version of M2M Data Format.

        :getter: Returns this parameter
        :type: :class:`str`
        """
        pass

    @abstractproperty
    def data_id(self):
        """'data_id' of this M2M Data.

        :getter: Returns this parameter
        :type: :class:`str`
        """
        pass

    @property
    def info_summary(self):
        return self._info_summary

    @info_summary.setter
    def info_summary(self, value):
        self._info_summary = value

    @abstractproperty
    def device_info(self):
        """'device info' part.

        :getter: Returns this parameter
        :type: :class:`dict`
        """
        pass

    @abstractproperty
    def data_schema(self):
        """'data schema' part.

        :getter: Returns this parameter
        :type: :class:`list`
        """
        pass

    @property
    def data_units(self):
        units = {}
        for value_schema in self.data_schema:
            if 'unit' in value_schema:
                units[value_schema['name']] = value_schema['unit']
        return units

    @property
    def primary_keys(self):
        """Primary keys for this M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`list`
        """
        return self._primary_keys

    @primary_keys.setter
    def primary_keys(self, value):
        self._primary_keys = value

    def get_pk_values(self, datum):
        """Returns primary keys with datum value.

        :param datum: Datum belong to this M2M Data.
        :rtype: :class:`dict`
        """
        pk_values = {}
        for pk in self.primary_keys:
            if pk in datum:
                pk_values[pk] = datum[pk]
            elif pk in self.device_info:
                pk_values[pk] = self.device_info[pk]
        return pk_values

    @abstractproperty
    def data_values(self):
        """'data'->'values' part.

        :getter: Returns this parameter
        :type: :class:`dict`
        """
        pass

    @property
    def size(self):
        """Number of datum in this M2M Data.

        :getter: Returns this parameter
        :type: :class:`int`
        """
        return len(self.data_values)

    @abstractproperty
    def min_time(self):
        """Minimum time of datum.

        :getter: Returns this parameter
        :type: :class:`str` (ISO 8601 format)
        """
        pass

    @abstractproperty
    def max_time(self):
        """Minimum time of datum.

        :getter: Returns this parameter
        :type: :class:`str` (ISO 8601 format)
        """
        pass

    @abstractproperty
    def south(self):
        """Minimum latitude value of datum.

        :getter: Returns this parameter
        :type: :class:`float`
        """
        pass

    @abstractproperty
    def north(self):
        """Maximum latitude value of datum.

        :getter: Returns this parameter
        :type: :class:`float`
        """
        pass

    @abstractproperty
    def west(self):
        """Minimum longitude value of datum.

        :getter: Returns this parameter
        :type: :class:`float`
        """
        pass

    @abstractproperty
    def east(self):
        """Maximum longitude value of datum.

        :getter: Returns this parameter
        :type: :class:`float`
        """
        pass

    @property
    def dict(self):
        """dict type expressions of this M2M Data.

        :getter: Returns this parameter
        :type: :class:`dict`
        """
        return self._dict

    @property
    def json(self):
        """JSON text type expressions of this M2M Data.

        :getter: Returns this parameter
        :type: :class:`str`
        """
        # return json.dumps(self._dict, ensure_ascii=False)  # FIXME
        return json.dumps(self._dict)

    @property
    def metadata_dict(self):
        return {'primary': self.dict['primary'], 'sensor_info': self.dict['sensor_info']}

    @property
    def metadata_json(self):
        # return json.dumps(self.metadata_dict, ensure_ascii=False)  # FIXME
        return json.dumps(self.metadata_dict)

    @property
    def data_dict(self):
        return {'data': self.dict['data']}

    @property
    def data_json(self):
        # return json.dumps(self.data_dict, ensure_ascii=False)  # FIXME
        return json.dumps(self.data_dict)

    def append(self, datum):
        """Append datum to this M2M Data.

        :param dict datum: Datum
        :return: None
        """
        self.data_values.append(datum)

    def extend(self, data):
        """Extend this M2M Data with argument data.

        :param list data: List of datum
        :return: None
        """
        self.data_values.extend(data)

    def commit(self):
        """Change commit state to True.

        :return: None
        """
        assert self._is_commit is False
        self._is_commit = True

    @property
    def is_commit(self):
        """Commit state.

        :getter: Returns this parameter
        :type: :class:`bool`
        """
        return self._is_commit

    @abstractmethod
    def accept(self, visitor):
        """Accept M2MDataVisitor object to do something about this M2MData.

        :param M2MDataVisitor visitor: M2MDataVisitor object.
        :return: Process result by visitor.
        :rtype: :class:`object`
        """
        pass


class M2MDataV101(M2MData):
    """Implementation of M2MData class as M2M Data Format v1.01.
    """

    def __getitem__(self, i):
        return self.data_values[i]

    def __init__(self):
        super(M2MDataV101, self).__init__()
        self._dict = M2MDataV101.DEFAULT_DICT

    def version(self):
        """Implementation of abstractproperty.
        """
        return '1.01'

    @property
    def data_id(self):
        """Implementation of abstractproperty.
        """
        return self._dict['sensor_info']['data_link']['data_id']

    @property
    def device_info(self):
        """Implementation of abstractproperty.
        """
        return self._dict['sensor_info']['device_info']

    @property
    def data_schema(self):
        """Implementation of abstractproperty.
        """
        return self._dict['sensor_info']['schema']

    @property
    def data_values(self):
        """Implementation of abstractproperty.
        """
        return self._dict['data']['values']

    @property
    def min_time(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            time = dateutil.parser.parse(datum['time']+self._dict['primary']['timezone'])
            if result is None or time < result:
                result = time
        return result

    @property
    def max_time(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            time = dateutil.parser.parse(datum['time']+self._dict['primary']['timezone'])
            if result is None or result < time:
                result = time
        return result

    @property
    def south(self):
        """Implementation of abstractproperty.
        """
        if 'latitude' in self.device_info:
            return self.device_info['latitude']
        else:
            return None

    @property
    def north(self):
        """Implementation of abstractproperty.
        """
        return self.south

    @property
    def west(self):
        """Implementation of abstractproperty.
        """
        if 'longitude' in self.device_info:
            return self.device_info['longitude']
        else:
            return None

    @property
    def east(self):
        """Implementation of abstractproperty.
        """
        return self.west

    @property
    def data_values(self):
        """Implementation of abstractproperty.
        """
        return self._dict['data']['values']

    def accept(self, visitor):
        """Implementation of abstractproperty.
        """
        return visitor.visit_v101(self)

    #: Default parameters
    DEFAULT_DICT = {
        "primary": {
            "format_version": 1.01,
            "title": None,
            "provenance": {
                "source": {
                    "info": None,
                    "contact": ""
                },
                "create_by": {
                    "contact": None,
                    "time": None
                }
            },
            "tag": "",
            "timezone": None,
            "security": "public",
            "id": None
        },
        "sensor_info": {
            "data_hash": None,
            "data_link": {
                "uri": None,
                "data_id": None
            },
            "data_format": "json",
            "device_info": {
                "name": None,
                "serial_no": None,
                "capability": {
                    "frequency": {
                        "count": None,
                        "type": None
                    }
                },
                "ownership": None,
                "ipaddress": None,
                "id": None
            },
            "data_profile": "Weather",
            "data_size": None,
            "schema": []
        },
        "data": {
            "values": [],
            "data_id": None
        }
    }


class M2MDataV102(M2MData):
    """Implementation of M2MData class as M2M Data Format v1.02.
    """

    def __getitem__(self, i):
        return self.data_values[i]

    def __init__(self):
        super(M2MDataV102, self).__init__()
        self._dict = M2MDataV102.DEFAULT_DICT

    def version(self):
        """Implementation of abstractproperty.
        """
        return '1.02'

    @property
    def data_id(self):
        """Implementation of abstractproperty.
        """
        return self._dict['sensor_info']['data_link']['data_id']

    @property
    def device_info(self):
        """Implementation of abstractproperty.
        """
        return self._dict['sensor_info']['device_info']

    @property
    def data_schema(self):
        """Implementation of abstractproperty.
        """
        return self._dict['sensor_info']['schema']

    @property
    def data_values(self):
        """Implementation of abstractproperty.
        """
        return self._dict['data']['values']

    @property
    def min_time(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            time = dateutil.parser.parse(datum['time']+self._dict['primary']['timezone'])
            if result is None or time < result:
                result = time
        return result

    @property
    def max_time(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            time = dateutil.parser.parse(datum['time']+self._dict['primary']['timezone'])
            if result is None or result < time:
                result = time
        return result

    @property
    def south(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            if result is None or datum['latitude'] < result:
                result = datum['latitude']
        return result

    @property
    def north(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            if result is None or result < datum['latitude']:
                result = datum['latitude']
        return result

    @property
    def west(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            if result is None or datum['longitude'] < result:
                result = datum['longitude']
        return result

    @property
    def east(self):
        """Implementation of abstractproperty.
        """
        result = None
        for datum in self.data_values:
            if result is None or result < datum['longitude']:
                result = datum['longitude']
        return result

    def accept(self, visitor):
        """Implementation of abstractproperty.
        """
        return visitor.visit_v102(self)

    #: Default parameters
    DEFAULT_DICT = {
        "primary": {
            "format_version": 1.02,
            "title": None,
            "provenance": {
                "source": {
                    "info": None,
                    "contact": ""
                },
                "create_by": {
                    "contact": None,
                    "time": None
                }
            },
            "tag": "",
            "timezone": None,
            "security": "public",
            "id": None
        },
        "sensor_info": {
            "data_hash": None,
            "data_link": {
                "uri": None,
                "data_id": None
            },
            "data_format": "json",
            "device_info": {
                "name": None,
                "serial_no": None,
                "capability": {
                    "frequency": {
                        "count": None,
                        "type": None
                    }
                },
                "ownership": None,
                "ipaddress": None,
                "id": None
            },
            "data_profile": "Weather",
            "data_size": None,
            "schema": []
        },
        "data": {
            "values": [],
            "data_id": None
        }
    }


def create_m2m_data_from_json(m2m_data_json):
    """

    :param m2m_data_json:
    :return:
    """
    m2m_data_dict = json.loads(m2m_data_json)
    return create_m2m_data_from_dict(m2m_data_dict)


def create_m2m_data_from_dict(m2m_data_dict):
    """

    :param m2m_data_dict:
    :return:
    """
    if m2m_data_dict['primary']['format_version'] == 1.01:
        m2m_data = M2MDataV101()
    elif m2m_data_dict['primary']['format_version'] == 1.02:
        m2m_data = M2MDataV102()
    else:
        raise AssertionError()

    m2m_data._dict = m2m_data_dict
    return m2m_data