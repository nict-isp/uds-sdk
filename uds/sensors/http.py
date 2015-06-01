# -*- coding: utf-8 -*-
"""
uds.sensors.http
~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""

import datetime
import urllib
import urllib2
from abc import abstractmethod

import uds.logging
from uds.sensors.base import Sensor
from uds.utils.crawling import Pacemaker


class HttpSensor(Sensor):
    """
    
    """

    def __init__(self, project_home):
        super(HttpSensor, self).__init__(project_home)

        self._interval = 0
        self._pacemaker = None

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

    def open(self):
        """Override of super class's method.
        """
        super(HttpSensor, self).open()
        self._pacemaker = Pacemaker(self.interval)

    def fetch(self, timeout=20):
        """Fetch contents by use of HTTP protocol. (Overridden method)

        :param timeout: Time until HTTP access timeout.
        :return: WebPageSource object including content and url.
        """
        self._pacemaker.wait()

        url, post_data = self.create_request()
        encoded_data = _encode_post_data(post_data)

        if url is None or url == '':
            uds.logging.warning('[fetch] url for request is none or empty.')
            return False

        uds.logging.info('[fetch] --- start ----------------------------')

        proxies = {}
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/29.0.1547.66 ' \
                     'Safari/'
        # headers = { 'User-Agent' : user_agent }
        proxy_handler = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent', user_agent)]
        urllib2.install_opener(opener)
        # sock = _thread_timeout(func=opener.open, args=[self._url, self._postData, timeout], timeout_duration=timeout)

        try:
            uds.logging.info('[fetch] url=%s', url)
            sock = opener.open(url, encoded_data, timeout)
        except:
            sock = None
        if sock is None:
            uds.logging.error('[fetch] Get Open Error URL=%s', url)
            source = WebPageSource()
            source.url = url
            source.content = None
            return source

        http_source = _thread_timeout(sock.read, None, timeout)
        sock.close()

        # 文字コードをunicodeに変換
        try:
            html_unicode = unicode(http_source, "shift_jis")
        except:
            try:
                html_unicode = unicode(http_source, "euc-jp")
            except:
                try:
                    html_unicode = unicode(http_source, "utf-8")
                except:
                    html_unicode = http_source

        source = WebPageSource()
        source.url = url
        source.content = html_unicode
        return source

    @abstractmethod
    def create_request(self):
        """Create parameters for HTTP request in a single crawling cycle.

        :return:
            * **rul** 　-　 URL of data source
            * **post_data** 　-　  POST parameters
        :rtype: str, dict
        """
        pass

    def parse(self, source):
        """Override of super class's method.
        """
        return self.parse_content(source.content, source.url)

    @abstractmethod
    def parse_content(self, content, url):
        """Parse fetched contents to list of M2M Data.

        :param content: Fetched content by http access.
        :param url: Fetched content URL.
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass


class WebPageSource(object):
    """Fetch result object for HttpSensor.
    """
    def __init__(self):
        #: Content
        self.content = None
        #: URL of content
        self.url = None


def _encode_post_data(post_data):
    if post_data is None:
        return None
    else:
        return urllib.urlencode(post_data)


def _thread_timeout(func, args=(), timeout_duration=1, default=None):
    import threading

    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(args)
            except:
                self.result = default

    it = InterruptableThread()
    it.start()
    # print "Time duration:", timeout_duration
    it.join(timeout_duration)
    if it.isAlive():
        return default
    else:
        return it.result

