"""
uds.contrib
~~~~~~~~~~~

Extension point for extra or optional modules.

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""

# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

print "Initialize uds-sdk/uds/contrib"