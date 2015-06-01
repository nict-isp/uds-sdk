# -*- coding: utf-8 -*-
"""
uds.io.base
~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from abc import ABCMeta
from abc import abstractmethod


class IOClient(object):
    """

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class M2MDataDao(object):
    """

    """

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def reconnect(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def select_last(self, key_data):
        """

        :return:
        :rtype:
        """
        pass

    @abstractmethod
    def insert(self, m2m_data):
        """

        :param m2m_data:
        :return:
        :rtype:
        """
        pass
