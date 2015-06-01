# -*- coding: utf-8 -*-
"""
uds.logging
~~~~~~~~~~~

Implements the logging support for UDS.

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
from __future__ import absolute_import

import os
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler


_configured = False


def _create_logger(log_dir_path, logger_name, log_file_enabled, log_params):
    logger = logging.getLogger(logger_name)

    # Setup format
    formatter = Formatter(fmt='%(asctime)s %(levelname)7s: %(message)s', datefmt='%Y/%m/%d %p %I:%M:%S',)

    # Enable console output
    console = logging.StreamHandler()
    console.level = log_params['level']
    console.formatter = formatter
    logger.addHandler(console)

    # Enable file output with rotation
    if log_file_enabled:
        log_file_path = os.path.join(log_dir_path, logger_name + ".log")
        file_handler = RotatingFileHandler(
            filename=log_file_path,
            mode='a',
            maxBytes=log_params['max_bytes'],
            backupCount=log_params['backup_count']
        )
        file_handler.level = log_params['level']
        file_handler.formatter = formatter
        logger.addHandler(file_handler)

    logging.getLogger().setLevel(logging.DEBUG)

    return logger


def configure(logger_name, log_dir_path, log_file_enabled, log_params):
    """Configure uds.logging module.
    This function is called only once before running sensor.

    :param str log_dir_path: Directory path for writing log
    :param str logger_name: Name of logger instance
    :param bool log_file_enabled: enable/disable writing log to file
    :return: None
    """
    global _configured
    global _logger
    assert not _configured
    _logger = _create_logger(log_dir_path, logger_name, log_file_enabled, log_params)
    info("Open uds.logging module.")
    _configured = True


def debug(msg, *args, **kwargs):
    """Logs a message with level DEBUG.
    Same usage as in https://docs.python.org/2.7/library/logging.html .

    :param str msg: Message
    :param str args: Arguments
    :param kwargs: Keyword arguments
    :return: None
    """
    assert _logger is not None
    _logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """Logs a message with level INFO.
    Same usage as in https://docs.python.org/2.7/library/logging.html .

    :param msg: Message
    :param args: Arguments
    :param kwargs: Keyword arguments
    :return: None
    """
    assert _logger is not None
    _logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """Logs a message with level WARNING.
    Same usage as in https://docs.python.org/2.7/library/logging.html .

    :param msg: Message
    :param args: Arguments
    :param kwargs: Keyword arguments
    :return: None
    """
    assert _logger is not None
    _logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """Logs a message with level ERROR.
    Same usage as in https://docs.python.org/2.7/library/logging.html .

    :param msg: Message
    :param args: Arguments
    :param kwargs: Keyword arguments
    :return: None
    """
    assert _logger is not None
    _logger.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """Logs a message with level CRITICAL.
    Same usage as in https://docs.python.org/2.7/library/logging.html .

    :param msg: Message
    :param args: Arguments
    :param kwargs: Keyword arguments
    :return: None
    """
    assert _logger is not None
    _logger.critical(msg, *args, **kwargs)


# Set default logger
_logger = _create_logger(
    log_dir_path=None,
    logger_name='DefaultLoggerForUDS',
    log_file_enabled=False,
    log_params={
        'level': logging.INFO,
        'max_bytes': 1000 * 1000,
        'backup_count': 5
    }
)
