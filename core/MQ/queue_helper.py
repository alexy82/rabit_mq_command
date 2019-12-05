# coding=utf-8
import re
import logging
from logging import config as conf
import settings
from core.MQ.channel import CHANNEL_MANAGER


conf.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


class QueueHelper(object):

    def __init__(self, DICT, BIND_DICT):
        self.DICT = DICT
        self.BIND_DICT = BIND_DICT
        self.action_all = {
            'remove': self.remove_all,
            'declare': self.declare_all,
            'bind': self.bind_all,
            'purge': self.purge_all,
        }
        self.action = {
            'remove': self.remove,
            'declare': self.declare,
            'bind': self.bind,
            'purge': self.purge,
        }
        self.action_pattern = {
            'remove': self.remove_by_pattern,
            'purge': self.purge_by_pattern,
            'declare': self.declare_by_pattern,
            'bind': self.bind_by_pattern,
        }

    def declare(self, name):
        """"
        Declare queue with name(key) and config in settings.QUEUES
        :param name: key of queue in settings.QUEUES
        :return:
        """
        if name not in self.DICT:
            return False
        LOGGER.info('Declare queue {}'.format(name))
        queue_info = self.DICT[name]
        channel = CHANNEL_MANAGER.get_channel(queue_info)
        config = queue_info['config']
        channel.queue_declare(queue=name, **config)
        LOGGER.info('Queue {} is declared'.format(name))
        return True

    def bind(self, name):
        """"
        Bind queue to exchange with name_exchange, routing_key, arguments in settings.QUEUES
        :param name: key of queue in settings.QUEUES
        :return:
        """
        if name not in self.DICT:
            return False
        queue_info = self.DICT[name]
        channel = CHANNEL_MANAGER.get_channel(queue_info)
        list_exchange_bind = self.BIND_DICT[name]
        for config_bind in list_exchange_bind:
            try:
                LOGGER.info("Bind to exchange:[{}] with routing_key: [{}]".format(config_bind['exchange'],
                                                                                  config_bind['routing_key']))
                channel.queue_bind(queue=name, exchange=config_bind['exchange'],
                                   routing_key=config_bind['routing_key'], arguments=config_bind['arguments'])
            except:
                LOGGER.exception()
        return True

    def remove(self, name, if_unused=False, if_empty=False):
        queue_info = self.DICT[name]
        channel = CHANNEL_MANAGER.get_channel(queue_info)
        x = channel.queue_delete(queue=name, if_unused=if_unused, if_empty=if_empty)
        if x.method.NAME == 'Queue.DeleteOk':
            LOGGER.info('Deleted queue {} '.format(name))
            return True
        return False

    def purge(self, name):
        if name in self.DICT:
            queue_info = self.DICT[name]
            channel = CHANNEL_MANAGER.get_channel(queue_info)
            channel.queue_purge(name)
            LOGGER.info('Purge queue {} '.format(name))
            return True

        return False

    def declare_all(self):
        """"
        Declare all queues in settings.QUEUES
        :return:
        """
        LOGGER.info('Start declare queue...')
        for name in self.DICT:
            self.declare(name)

    def bind_all(self):
        """"
        Bind all queues in  settings.QUEUES
        :return:
        """
        LOGGER.info('Start bind all queue...')
        for name in self.DICT:
            self.bind(name)

    def remove_all(self):
        """"
        Remove all queues
        :return:
        """
        LOGGER.info('Start remove all queue...')
        for name in self.DICT:
            self.remove(name)

    def purge_all(self):
        LOGGER.info('Start purge all queue...')
        for name in self.DICT:
            self.purge(name)

    def remove_by_pattern(self, name_pattern, if_unused=False, if_empty=False):
        """"

        :param name_pattern: pattern is formatted by Regex
        :type name_pattern: str
        :param if_unused: Deleting when no Consumer connect queses
        :param if_empty: Deleting when they don't have message
        :return:
        """
        for name in self.DICT:
            if re.match(name_pattern, name):
                self.remove(name, if_unused=if_unused, if_empty=if_empty)

    def purge_by_pattern(self, name_pattern):
        for name in self.DICT:
            if re.match(name_pattern, name):
                self.purge(name)

    def declare_by_pattern(self, name_pattern):
        for name in self.DICT:
            if re.match(name_pattern, name):
                self.declare(name)

    def bind_by_pattern(self, name_pattern):
        for name in self.DICT:
            if re.match(name_pattern, name):
                self.bind(name)

    def get_queue_info(self, name):
        if name not in self.DICT:
            return None
        queue_info = self.DICT[name]
        return queue_info

