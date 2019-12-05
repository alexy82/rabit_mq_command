# coding=utf-8
import logging
from logging import config as conf
import settings
from core.MQ.channel import CHANNEL_MANAGER

conf.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


class ExchangeHelper(object):

    def __init__(self, DICT, BIND_DICT):
        self.DICT = DICT
        self.BIND_DICT = BIND_DICT
        self.action_all = {
            'remove': self.remove_all,
            'declare': self.declare_all,
            'bind': self.bind_all,
        }
        self.action = {
            'remove': self.remove,
            'declare': self.declare,
            'bind': self.bind,
        }

    def declare(self, name):
        """"
        declare exchanges with name and config in DICT
        :param name:
        :return:
        """
        if name not in self.DICT:
            return False
        LOGGER.info('Starting Declare exchange {}'.format(name))
        exchange_info = self.DICT[name]
        channel = CHANNEL_MANAGER.get_channel(exchange_info)
        config = exchange_info['config']
        exchange_type = exchange_info['type']
        channel.exchange_declare(exchange=name, exchange_type=exchange_type, **config)
        LOGGER.info('Exchange {} is declared'.format(name))
        return True

    def remove(self, name):
        if name not in self.DICT:
            return False
        exchange_info = self.DICT[name]
        channel = CHANNEL_MANAGER.get_channel(exchange_info)
        LOGGER.info('Remove exchange {}'.format(name))
        channel.exchange_delete(name)
        return True

    def bind(self, name):
        """"
        bind exchanges with name and config in BIND_DICT
        :param name:
        :return:
        """
        if name not in self.BIND_DICT or name not in self.DICT:
            return False
        exchange_info = self.DICT[name]
        channel = CHANNEL_MANAGER.get_channel(exchange_info)
        list_exchange_bind = self.BIND_DICT[name]
        for config_bind in list_exchange_bind:
            try:
                LOGGER.info("Bind exchange: [{}] to [{}] with routing_key: [{}]".format(name, config_bind['name'],
                                                                                        config_bind['routing_key']))
                channel.exchange_bind(source=name, destination=config_bind['name'],
                                      routing_key=config_bind['routing_key'], arguments=config_bind['arguments'])
            except:
                LOGGER.exception("Not found exchange {}".format(config_bind['name']))
        return True

    def declare_all(self):
        """
        Declare all Exchanges
        :return:
        """
        LOGGER.info('Start declare exchange...')
        for name in self.DICT:
            self.declare(name)

    def bind_all(self):
        """
        Bind all Exchanges
        :return:
        """
        LOGGER.info('Start bind exchange...')
        for name in self.BIND_DICT:
            self.bind(name)

    def remove_all(self):
        """
        Remove  all exchange in DICT
        :return:
        """
        LOGGER.info('Start remove all exchange...')
        for name in self.DICT:
            exchange_info = self.DICT[name]
            channel = CHANNEL_MANAGER.get_channel(exchange_info)
            LOGGER.info('Remove exchange {}'.format(name))
            channel.exchange_delete(name)


if __name__ == '__main__':
    import json

    with open('/vagrant/code/is_mq_manager/example_exchange_config.json') as f:
        data = json.load(f)
    obj = ExchangeHelper(data['declare'], data['bind'])
    obj.declare('is_mq_manager.minh')
