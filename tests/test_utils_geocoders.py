# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from uds.utils.geocoders import Geocoder


class TestGeocoders(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_str_to_loc_list(self):
        geocoder = Geocoder('../_cache')
        loc_list = geocoder.str_to_loc_list('東京')
        print loc_list
        assert loc_list is not False


if __name__ == "__main__":
    unittest.main()