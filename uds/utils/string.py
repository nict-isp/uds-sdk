# -*- coding: utf-8 -*-
"""
uds.utils.string
~~~~~~~~~~~~~~~~

Utility functions to parse string and others.

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import re
import dateutil.parser


def check_ignore(invalid_keyword_list, text):
    """Check the text validity as sensing data. (Check the text has invalid strings.)

    :param list invalid_keyword_list: List of invalid keywords
    :param str text: Text to check
    :return: If not contains invalid strings. If contains invalid strings, return False.
    """
    try:
        text = unicode(text, "utf-8")
    except StandardError:
        try:
            text = unicode(text, "shift_jis")
        except StandardError:
            try:
                text = unicode(text, "euc-jp")
            except StandardError:
                pass

    for keyword in invalid_keyword_list:
        if text.find(keyword) >= 0:
            return False
        else:
            pass
    return True


def try_parse_to_numeric(value):
    """Try parse the string to numeric value.
    If failed to parse, return None.

    :param str value: String value
    :return: Parse result
    :rtype: float
    """
    # 数値のみかチェック ------------------------------------------------------------
    try:
        # 数値の場合、OKとなるため、処理を終了する
        return float(value)
    except StandardError:
        pass

    # 数値のみを抜き出す ------------------------------------------------------------
    try:
        r = re.compile(r'(\d+\.*\d*)')
        numeric_list = r.findall(value)

        return float(numeric_list[0])

    except StandardError:
        return None


def try_parse_to_datetime(value, timezone_str=None):
    """Try parse the string to datetime format of ISO 8601.
    If failed to parse, return None.

    :param str value: Datetime as string value
    :param str timezone_str: Timezone as string
    :return: Datetime string as ISO 8601 format
    :rtype: str
    """
    # # タイムゾーンの設定
    # if timezone_str == None:
    # timezone = "+0000"
    # else:
    # timezone = timezone_str

    # 不要と思われる文字を削除する
    value = value.replace("]", "")
    value = value.replace("[", "")

    # 時刻データに変換可能かチェック ------------------------------------------------------
    try:
        date_value = dateutil.parser.parse(value)
    except StandardError:
        value = re.sub(r'[a-zA-Z[\]]', ' ', value)
        date_value = dateutil.parser.parse(value)

        # yyyy-MM-ddTHH:MM:ss.SSS
        # の形式で返す
        # isoformat()を使用したかったが、微妙にフォーマットが異なる
        # 2012-01-13 00:00:00.000000-05:00
        # ~~~3桁削る必要がある
    # return "%04d-%02d-%02dT%02d:%02d:%02d.%03d%s" % (datevalue.year, datevalue.month, datevalue.day, datevalue.hour, datevalue.minute, datevalue.second, datevalue.microsecond / 1000, timezone)
    return "%04d-%02d-%02dT%02d:%02d:%02d.%03d" % (
        date_value.year, date_value.month, date_value.day, date_value.hour, date_value.minute, date_value.second,
        date_value.microsecond / 1000)


def try_parse_to_string(value):
    """Try parse the string to effective string.
    If failed to parse, return None.

    * If the argument value is None, return None.
    * If the argument value is ''(empty string), return None.
    * Parse string u'\\\\xa0' to ' '(space).

    :param str value: String value
    :return: Parse result
    :rtype: str
    """
    if value is None:
        return value

    try:
        value = str(value.replace(u'\xa0', ' ').strip())
    except StandardError:
        value = value.replace(u'\xa0', ' ').strip().encode('utf-8')

    if value == '':
        return None
    else:
        return value
