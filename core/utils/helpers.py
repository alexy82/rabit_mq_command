# coding=utf-8
"""
Uncategorized utility helpers
"""
import traceback
from datetime import datetime

import importlib
import pytz

from settings import TIME_ZONE


def format_exc_info(exc_info):
    """
    Format exception info as string
    :param exc_info: exception info
    :return: string
    """
    if exc_info[0] is None:
        return 'None'
    lines = traceback.format_exception(*exc_info)
    return ''.join(line for line in lines)


def import_class_by_path(class_path: str):
    """
    Import class by path
    :param class_path: module path of class
    :return: Class

    :example:
        import_class_by_path('core.db.DatabaseClass')
    """
    class_path = class_path.split('.')
    class_name = class_path.pop()
    module_path = '.'.join(class_path)
    module = importlib.import_module(module_path)
    class_ = getattr(module, class_name)
    return class_


def parse_str(value, length=None, default=None, from_right=False):
    """
    Class method to parse string with max length and default value
    :param value: value needs setting
    :param length: max length of field to be trimmed
    :param default: default value if value is None
    :return:
    """
    if value is None:
        value = default
    if isinstance(value, str) and length is not None and length >= 0:
        if from_right:
            value = value[-length:]
        else:
            value = value[:length]
    return value


def change_timezone(dt: datetime = None, fromtz: str = 'UTC', totz: str = TIME_ZONE):
    """
    Change timezone
    :param dt:
    :param fromtz:
    :param totz:
    :return:
    """
    fromtz = pytz.timezone(fromtz)
    totz = pytz.timezone(totz)
    if dt is None:
        dt = datetime.now(fromtz)
    else:
        dt = fromtz.localize(dt)
    dt = dt.astimezone(totz)
    return dt
