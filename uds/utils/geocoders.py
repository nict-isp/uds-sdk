# -*- coding: utf-8 -*-
"""
uds.utils.geocoders
~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import os
from placemaker import placemaker

import uds.logging


class Geocoder:
    """A geocoding utility by use of Yahoo Placemaker API (https://developer.yahoo.com/boss/geo/).

    :param cache_dir: Path of directory to cache geocoded data.
    """

    def __init__(self, cache_dir):
        assert os.path.exists(cache_dir)

        geo_cache_dir = os.path.join(cache_dir, 'GeoCoding_Error_Logs')
        if not os.path.exists(geo_cache_dir):
            os.mkdir(geo_cache_dir)

        self._yahoo_placemaker = placemaker("42yLC63V34GbbzyAWtgkdbeYfAJM54.CIECCgqe504lwWe4VUHcBiOrHJSeqLVJ0OYK3aw--")

    def str_to_loc_list(self, text, engine='Yahoo'):
        """Geocode the text to location list.

        :param str text:
        :param str engine: Geocoding engine type. ('Yahoo' is available. )
        :return: location as dictionary.

                  * loc["place"] : Place name
                  * loc["longitude"] : longitude value
                  * loc["latitude" ] : latitude value

        :rtype: dict
        """

        if engine.lower() == 'Yahoo'.lower():
            loc_list = self._str_to_loc_list_yahoo(text)
        else:
            raise AssertionError('Invalid argument engine=%s', engine)

        if len(loc_list) < 1:
            uds.logging.warning("[geocoder] > Geocoding Failure! Results is none.")
            return False

        if len(loc_list) == 1:
            return loc_list[0]

        if len(loc_list) > 1:
            uds.logging.warning("[geocoder] > Geocoding Failure! Results is too many.")
            return False
        
        return loc_list

    def _str_to_loc_list_yahoo(self, text):
        """Geocode the text to location list by use of Yahoo Placemaker API.
        """
        try:
            self._yahoo_placemaker.find_places(text.encode('utf_8').replace("<b>", "").replace("</b>", ""))
        except Exception as e:
            uds.logging.error('[geocodere] self._yahoo_placemaker %s', str(e))
        
        loc_list = []
        if self._yahoo_placemaker.places is not []:
            for place in self._yahoo_placemaker.places:
                loc = {}
                loc["place"] = place.name
                loc["longitude"] = place.centroid.longitude
                loc["latitude"] = place.centroid.latitude
                loc_list.append(loc)
        
        return loc_list

