# -*- coding: utf-8 -*-
"""
uds.data.build
~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import copy

import uds.utils.dict
from uds.data import M2MDataV101
from uds.data import M2MDataV102
from uds.data import M2MDataVisitor


class M2MDataBuilder(M2MDataVisitor):
    """M2MDataBuilder build M2MData object with any parameters
    like 'title', 'timezone' and others.
    """

    def __init__(self):
        super(M2MDataVisitor, self).__init__()
        self._title = None
        self._timezone = None
        self._m2m_info = None
        self._m2m_data_schema = None
        self._primary_keys = None

    @property
    def title(self):
        """Title to set to M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def timezone(self):
        """Timezone to set to M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`str`
        """
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value

    @property
    def m2m_info(self):
        """Default information values of metadata part to set to M2M Data.

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
        """Data schema definition of data part to set to M2M Data.

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
        """Primary keys to set to M2M Data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: :class:`list`
        """
        return self._primary_keys

    @primary_keys.setter
    def primary_keys(self, value):
        self._primary_keys = value

    def create_m2m_data(self):
        """Create M2MData object.

        :rtype: :class:`uds.data.M2MData`
        """
        if self.m2m_info['formatVersion'] == '1.01':
            m2m_data = M2MDataV101()
        elif self.m2m_info['formatVersion'] == '1.02':
            m2m_data = M2MDataV102()
        else:
            raise AssertionError("'formatVersion' is invalid.")

        m2m_data = self.process(m2m_data)
        return m2m_data

    def visit_v101(self, m2m_data):
        """Implementation of abstractmethod --- Initialize v1.01 M2MData.

        :param M2MDataV101 m2m_data: Build target
        :rtype: :class:`uds.data.M2MDataV101`
        """
        built = copy.deepcopy(m2m_data)
        built.dict['primary']['title'] = self.title
        built.dict['primary']['timezone'] = self.timezone

        if 'srcContact' in self._m2m_info:
            built.dict['primary']['provenance']['source']['contact'] = self.m2m_info['srcContact']

        assert 'createdContact' in self.m2m_info
        built.dict['primary']['provenance']['create_by']['contact'] = self.m2m_info['createdContact']

        if 'security' in self._m2m_info:
            built.dict['primary']["security"] = self.m2m_info['security']

        if 'tag' in self._m2m_info:
            built.dict['primary']["tag"] = self.m2m_info['tag']

        if 'device' in self._m2m_info:
            built.dict['sensor_info']['device_info'] = uds.utils.dict.override_dict(
                self.m2m_info['device'],
                built.dict['sensor_info']['device_info']
            )

        built.dict['sensor_info']['schema'] = self.m2m_data_schema
        built.primary_keys = self.primary_keys
        built.info_summary = self.m2m_info
        return built

    def visit_v102(self, m2m_data):
        """Implementation of abstractmethod --- Initialize v1.02 M2MData.

        :param M2MDataV102 m2m_data: Build target
        :rtype: :class:`uds.data.M2MDataV102`
        """
        # Same as v101
        return self.visit_v101(m2m_data)
