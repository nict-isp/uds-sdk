# -*- coding: utf-8 -*-
"""
uds.utils.crawling
~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from __future__ import absolute_import

import time
import datetime

import uds.logging


class Pacemaker(object):
    """

    """

    def __init__(self, interval=0):
        self._interval = interval
        self._before_datetime = None

    def wait(self):
        # 現在の時刻を取得
        now_datetime = datetime.datetime.now()

        if not self._before_datetime:
            # Not sleep at initial time
            pass
        else:
            # 前回取得からの差分を計算
            diff_datetime = self._before_datetime - now_datetime
            sleep_time = diff_datetime.total_seconds() + int(self._interval)

            if sleep_time > 0:
                # interval経過するまでwaitする
                uds.logging.info("Sleep time %ss", sleep_time)
                time.sleep(sleep_time)

        self._before_datetime = datetime.datetime.now()  # 現在の時刻を保存
