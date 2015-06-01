# -*- coding:utf-8 -*-
"""
uds.sensors.ieee1888
~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import random
import datetime
from abc import abstractmethod

from suds.client import Client
from suds.plugin import MessagePlugin

import uds.logging
from uds.sensors.base import Sensor
from uds.utils.crawling import Pacemaker


class BugfixMessagePlugin(MessagePlugin):
    """Plugin for bug fix.
    """
    def marshalled(self, context):
        # transport要素の namespace が http://soap.fiap.org/ となってしまうのを
        # http://gutp.jp/fiap/2009/11/ へ修正する。
        tp = context.envelope.childAtPath('Body/queryRQ/transport')
        tp.setPrefix(tp.findPrefix('http://gutp.jp/fiap/2009/11/'))


myplugins = (
    BugfixMessagePlugin(),)


class IEEE1888Sensor(Sensor):
    """

    """

    def __init__(self, project_home):
        super(IEEE1888Sensor, self).__init__(project_home)

        self._interval = 0
        self._pacemaker = None

        self._wsdl_url = None
        self._client = None

    @property
    def interval(self):
        """Second-scale interval of fetching data.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: int
        """
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def wsdl_url(self):
        """WSDL Address of SOAP protocol.

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: str
        """
        return self._wsdl_url

    @wsdl_url.setter
    def wsdl_url(self, value):
        self._wsdl_url = value

    def open(self):
        """Override of super class's method.
        """
        super(IEEE1888Sensor, self).open()
        self._pacemaker = Pacemaker(self.interval)
        self._client = Client(self._wsdl_url, cache=None, plugins=myplugins)

    def fetch(self):
        """Fetch data by use of IEEE 1888 protocol.

        :return: Response object of IEEE 1888 request.
        :rtype: dict
        """
        self._pacemaker.wait()

        if self._wsdl_url is None:
            uds.logging.error('[fetch] uds_url is necessary for you to do call')
            return False

        print str(datetime.datetime.today()) + " --- get start ----------------------------"

        response = self._send_query()

        return response

    def _send_query(self):
        query = {"_type": "storage", "_id": self._create_id(), "key": self.create_query_keys()}
        header = {"query": query}
        transport = {"header": header}

        try:
            response = self._client.service.query(transport)
            result = response
            while response.header.query.__dict__.has_key('_cursor'):
                query["_cursor"] = result.header.query['_cursor']
                response = self._client.service.query(transport)
                result.body.point.extend(response.body.point)
            return result
        except Exception, e:
            uds.logging.error('[fetch] %s', e)
            return None

    @staticmethod
    def _create_id():
        # <s:pattern value="[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"/>
        return '{0}-{1}-{2}-{3}-{4}'.format(
            hex(random.randint(0, 0xffffffff)).replace("0x", "", 1).replace("L", "", 1).zfill(8),
            hex(random.randint(0, 0xffff)).replace("0x", "", 1).zfill(4),
            hex(random.randint(0, 0xffff)).replace("0x", "", 1).zfill(4),
            hex(random.randint(0, 0xffff)).replace("0x", "", 1).zfill(4),
            hex(random.randint(0, 0xffffffffffff)).replace("0x", "", 1).replace("L", "", 1).zfill(12)
        )

    @abstractmethod
    def create_query_keys(self):
        """Create query keys for IEEE 1888 request.

        Example of query key::

            key1 = {
                '_attrName' :'time',
                '_id' : 'http://ieee1888.example.com/weather/01001/airtmp',
                '_select' : 'maximum'
            }

            key2 = {
                '_attrName': 'time',
                '_id': 'http://ieee1888.example.com/weather/01001/apress',
                '_lt': '2013-10-02 00:00:00+09:00',
                '_gteq': '2013-10-01 23:00:00+09:00'
            }

        :return: Query keys
        :rtype: dict
        """
        pass

    def parse(self, source):
        """Override of super class's method.
        """
        return self.parse_response(source)

    @abstractmethod
    def parse_response(self, response):
        """Parse IEEE 1888 response to M2M Data.

        :param dict response: IEEE 1888 response object
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass
