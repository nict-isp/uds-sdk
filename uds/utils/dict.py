# -*- coding: utf-8 -*-
"""
uds.utils.dict
~~~~~~~~~~~~~~

Utility functions to parse string and others.

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import copy


def override_dict(new, old):
    """Override old dict object with new one.

    :param object new: New dict
    :param object old: Nld dict
    :return: Overridden result
    :rtype: :attr:`object`
    """
    if isinstance(new, dict):
        merged = copy.deepcopy(old)
        for key in new.keys():
            if key in old:
                merged[key] = override_dict(new[key], old[key])
            else:
                merged[key] = new[key]
        return merged
    else:
        return new
