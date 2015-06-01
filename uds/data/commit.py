# -*- coding: utf-8 -*-
"""
uds.data.commit
~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import re
import copy
import json
import hashlib
import dateutil.parser
import datetime
import uds.utils.datetime

from uds.utils.datetime import normalize_timezone
from uds.data import M2MDataVisitor


class M2MDataCommitter(M2MDataVisitor):
    """M2MDataCommitter process the M2MData object, then set 'data_id', 'data_size' and other.

    """

    def __init__(self):
        pass

    def visit_v101(self, m2m_data):
        """Commit v1.01 M2M Data.
        
        :param M2MDataV101 m2m_data: Commit target
        :return: Committed M2M Data
        :rtype: :class:`uds.data.M2MDataV101`
        """
        # Calculate data_id
        committed = copy.deepcopy(m2m_data)
        date_time_now = datetime.datetime.now()
        data_id = m2m_data.dict['primary']['title'] + date_time_now.strftime('%Y%m%d%H%M%S') + "%06d" % date_time_now.microsecond

        # Normalize time offset.
        if 'timeOffset' in m2m_data.device_info:
            # For deprecated spec.
            m2m_data.dict['primary']['timezone'] = normalize_timezone(m2m_data.device_info.pop('timeOffset'))
        else:
            m2m_data.dict['primary']['timezone'] = normalize_timezone(m2m_data.dict['primary']['timezone'])

        # Commit data part.
        committed.dict['data']['data_id'] = data_id

        # Commit primary part.
        committed.dict['primary']['provenance']['create_by']['time'] = uds.utils.datetime.get_now_time(m2m_data.dict['primary']['timezone'])
        committed.dict['primary']["id"] = "http://m2m.nict.go.jp/m2m_data/?id=" + data_id

        # Commit sensor_info part.
        committed.dict['sensor_info']['data_size'] = len(m2m_data.data_json)
        json_data = json.dumps(committed.dict['data'])
        committed.dict['sensor_info']['data_hash'] = hashlib.md5(json_data).hexdigest()
        committed.dict['sensor_info']['data_link']['uri'] = 'next_data'
        committed.dict['sensor_info']['data_link']['data_id'] = data_id

        return committed

    def visit_v102(self, m2m_data):
        """Commit v1.02 M2M Data.
        
        :param M2MDataV102 m2m_data: Commit target
        :return: Committed M2M Data
        :rtype: :class:`uds.data.M2MDataV102`
        """
        # Same as v101
        return self.visit_v101(m2m_data)