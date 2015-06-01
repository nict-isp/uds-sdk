# -*- coding:utf-8 -*-
"""
uds.sensors.twitter
~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import re
import json
import Queue
from abc import abstractmethod
import tweepy

from uds.sensors.base import Sensor


class GetStreamingListener(tweepy.streaming.StreamListener):
    def __init__(self):
        tweepy.streaming.StreamListener.__init__(self)
        self._japanese_keyword_filter = None
        self._queue = None
        self._id_buffer = []

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, value):
        self._queue = value

    @property
    def japanese_keyword_filter(self):
        return self._japanese_keyword_filter

    @japanese_keyword_filter.setter
    def japanese_keyword_filter(self, value):
        if value is not None:
            self._japanese_keyword_filter = []
            for keyword in value:
                self._japanese_keyword_filter.append(re.compile(unicode(keyword)))

    def on_data(self, data_string):
        data_dict = json.loads(data_string)

        # If location is none, not enqueue.
        if 'created_at' in data_dict and data_dict['geo'] is None:
            return

        # Delete overlap data.
        if 'id_str' in data_dict and self._is_overlap_tweet(data_dict):
            return

        # Ignore deleted tweet
        if 'delete' in data_dict:
            return

        # Search japanese key words.
        if self._japanese_keyword_filter is not None:
            try:
                search_result = False
                for keywordFilter in self._japanese_keyword_filter:
                    if keywordFilter.search(data_dict['text']) is not None:
                        search_result = True
                        break

                if search_result is False:
                    return
            except:
                pass

        print 'Get Tweet Data ----------------- queue num = {0}'.format(self._queue.qsize())
        self._queue.put(data_string)

    def _is_overlap_tweet(self, data_dict):
        tweet_id = data_dict['id_str']
        if tweet_id in self._id_buffer:
            print "Ignore overlap tweet. tweet_id=" + tweet_id
            return True
        else:
            if len(self._id_buffer) >= 1000:
                self._id_buffer.pop(0)
            self._id_buffer.append(tweet_id)
            return False


class TwitterSensor(Sensor):
    """
    TwitterSensor Fetches Tweet data from Twitter using the Twitter Streaming APIs.
    """

    #: URI of Twitter Streaming API
    URI = 'stream.twitter.com'

    def __init__(self, project_home):
        super(TwitterSensor, self).__init__(project_home)

        self.filter_type = 'limited_buffer_filter'

        self._consumer_key = None
        self._consumer_secret = None
        self._access_key = None
        self._access_secret = None

        self._location_filter = None
        self._keyword_filter = None
        self._japanese_keyword_filter = None

        self._stream = None
        self._raw_data_queue = Queue.Queue()

    def set_auth_params(self, consumer_key, consumer_secret, access_key, access_secret):
        """Sets authentication parameters.

        :param consumer_key: Consumer key of twitter application.
        :param consumer_secret: Consumer secret of twitter application.
        :param access_key: Access key of twitter application for each twitter account.
        :param access_secret: Access secret of twitter application for each twitter account.
        :return: None.
        """
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_key = access_key
        self._access_secret = access_secret

    @property
    def location_filter(self):
        """Location filter to only collect Tweet data within a specified geographical area.
        See `Tweepy`_'s filter documentation for details.

        .. _Tweepy: http://tweepy.readthedocs.org/en/v3.3.0/streaming_how_to.html

        Example usage::

            location_filter = [122.933611, 20.425277, 153.986388, 45.557777]

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: list
        """
        return self._location_filter

    @location_filter.setter
    def location_filter(self, value):
        self._location_filter = value

    @property
    def keyword_filter(self):
        """Keyword filter to only collect Tweet data that includes the specified keywords.
        See `Tweepy`_'s filter documentation for details.

        .. _Tweepy: http://tweepy.readthedocs.org/en/v3.3.0/streaming_how_to.html

        Example usage::

            keyword_filter = ['rain Rain', 'typhoon hurricane', 'Japan,USA']

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: list
        """
        return self._keyword_filter

    @keyword_filter.setter
    def keyword_filter(self, value):
        self._keyword_filter = value

    @property
    def japanese_keyword_filter(self):
        """Japanese keyword filter to only collect Tweet data that includes the specified Japanese keywords.

         *  As shown below, specify keywords as a list of values and the resulting search
            will combine them with logical OR operators.

         *  Regular expression is available for search.

         Example usage::

            japanese_keyword_filter = ['雨', '風', '雪', '雲', 'くもり', '嵐', '暑', '寒']

        :getter: Returns this parameter
        :setter: Sets this parameter
        :type: list
        """
        return self._japanese_keyword_filter

    @japanese_keyword_filter.setter
    def japanese_keyword_filter(self, value):
        self._japanese_keyword_filter = value

    def open(self):
        super(TwitterSensor, self).open()

        # Create OAuthHandler
        auth = tweepy.auth.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_key, self._access_secret)

        # Create GetStreamingListener
        listener = GetStreamingListener()
        listener.japanese_keyword_filter = self._japanese_keyword_filter
        listener.queue = self._raw_data_queue

        self._stream = tweepy.streaming.Stream(auth, listener, secure=True)

        if self._location_filter is None and self._keyword_filter is None:
            # Fetches sample data provided by Twitter if you have not configured a filter
            self._stream.sample(async=True)
            print 'Set Sample'
        else:
            # Collects filtered Tweet data if you have configured a filter
            self._stream.filter(track=self._keyword_filter, locations=self._location_filter, async=True)
            print 'Set Location          Filter {0}'.format(self._location_filter)
            print 'Set Keyword           Filter {0}'.format(self._keyword_filter)
            print 'Set Japanese Keyword  Filter {0}'.format(self._japanese_keyword_filter)

    def close(self):
        super(TwitterSensor, self).close()
        self._stream.disconnect()

    def fetch(self):
        """Overridden method.

        :return: Response of Twitter Streaming API.
        :rtype: dict
        """
        json_data = self._raw_data_queue.get()
        print '[StreamSensor.Get] Dequeue ----- queue num = {0}'.format(self._rawdata_queue.qsize())
        return json_data

    def parse(self, source):
        """Overridden method.
        """
        return self.parse_data(source)

    @abstractmethod
    def parse_data(self, data):
        """Parse tweet data to list of M2M Data.

        :param dict data: Response of Twitter Streaming API.
        :return: list of M2M Data
        :rtype: list of :class:`uds.data.M2MData`
        """
        pass
