Installation
============

Installing Library Dependencies
-------------------------------

.. _Python: http://www.python.org
.. _pip: http://www.pip-installer.org/en/latest/installing.html
.. _easy_install: http://pypi.python.org/pypi/setuptools
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _lxml: http://lxml.de/
.. _MySQLdb: https://pypi.python.org/pypi/MySQL-python/1.2.5
.. _python-placemaker: https://github.com/bycoffe/python-placemaker


You need to install the following libraries before the UDS SDK.

*   `Python`_ 2.7 (Setting up Python default encoding to 'utf-8')

*   `pip`_ and `setuptools`_ Python packages. Nowadays `pip`_ requires and
    installs `setuptools`_ if not installed.

*   `lxml`_. Most Linux distributions ships prepackaged versions of lxml.
    Otherwise refer to http://lxml.de/installation.html

*   `MySQLdb`_. Most Linux distributions ships prepackaged versions of MySQLdb.
    Otherwise refer to https://pypi.python.org/pypi/MySQL-python/1.2.5

*   `python-placemaker`_.
    Refer to https://github.com/bycoffe/python-placemaker

.. note::

   Check :ref:`intro-install-platform-notes` .


Setting Up virtualenv
---------------------

**If necessary**, use virtualenv to set up a virtual environment for UDS development.
This allows you to create independent UDS development environments
and even switch between multiple versions of the UDS SDK.

Run the following command to create a virtual environment named 'myprojects'.

::

    $ mkdir myprojects
    $ cd myprojects
    $ virtualenv venv

Next, activate the virtual environment that you just created.
On OS X or Linux, run the following command.

::

    $ . venv/bin/activate

On Windows, run the following command.

::

    $ venv\scripts\activate

Installing the UDS SDK
----------------------

Using pip, install the UDS SDK directly from its GitHub repository.

::

    $ pip install git+http://github.com/nict-isp/uds-sdk.git



Checking Your UDS SDK Installation
----------------------------------

Once you have successfully installed the UDS SDK,
you will be able to use the :attr:`uds` command from a shell prompt.

#.  Check the UDS SDK version.
    ::

        $ uds --version

#.  Show the UDS SDK help message.
    ::

        $ uds --help


Uninstalling the UDS SDK
------------------------

You can use pip to uninstall the UDS SDK.
::

    $ pip uninstall uds-sdk



.. _intro-install-platform-notes:



Platform specific installation notes
------------------------------------

Ubuntu 12.0 or above
::::::::::::::::::::

*   Install `lxml`_ via apt-get.
    ::

        $ sudo apt-get install python-lxml

*   Install `MySQLdb`_ via apt-get.
    ::

        $ sudo apt-get install python-mysqldb

*   Install `python-placemaker`_ via pip.
    ::

        $ pip install git+https://github.com/bycoffe/python-placemaker.git

*   Setting up Python default encoding. Edit python setting file as follows.
    ::

        $ vi /usr/lib/python2.7/site.py

    Change encoding 'ascii' to 'utf-8' as follows.
    ::

        encoding = "ascii" # Default value set by _PyUnicode_Init()
            ↓
        encoding = "utf-8" # Default value set by _PyUnicode_Init()


