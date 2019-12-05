# coding=utf-8
import copy

import pika
import logging
from logging import config

from pika.spec import BasicProperties

import settings
from core.MQ.connection import CONNECTION_MANAGER

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


class BasicPublisher(object):
    channel = None
    connection_name = None
    type = None
    basic_properties = {
        'content_type': None,
        'content_encoding': None,
        'headers': None,
        'delivery_mode': None,
        'priority': None,
        'correlation_id': None,
        'reply_to': None,
        'expiration': None,
        'message_id': None,
        'timestamp': None,
        'type': None,
        'user_id': None,
        'app_id': None,
        'cluster_id': None
    }

    def __init__(self, content):
        self.connection_name = content
        self.connection = CONNECTION_MANAGER.get_connection(self.connection_name)

    def get_channel(self) -> pika.adapters.blocking_connection.BlockingChannel:
        if self.channel is None or not self.channel.is_open:
            if not self.connection.is_open:
                self.connection = CONNECTION_MANAGER.get_connection(self.connection_name)
            self.channel = self.connection.channel()
        return self.channel

    def publish(self, routing_key, exchange, body, properties=None):
        final_properties = copy.deepcopy(self.basic_properties)
        if properties is not None:
            for extra_property in properties:
                if extra_property in final_properties.keys():
                    final_properties[extra_property] = properties[extra_property]
        LOGGER.info('Sending message to exchange:\t[{}]  with routing_key \t[{}]'.format(exchange, routing_key))
        try:
            self.channel = self.get_channel()
            self.channel.publish(body=body,
                                 exchange=exchange,
                                 routing_key=routing_key,
                                 properties=BasicProperties(**final_properties))
        except:
            LOGGER.exception('Failed to start connection {connection_name} | routing key {routing_key}'
                             .format(connection_name=self.connection_name, routing_key=routing_key))
        finally:
            self.channel.close()


class Publisher(BasicPublisher):
    # TODO: Pass msg or callback to emit msg
    pass


if __name__ == '__main__':
    publisher = BasicPublisher()
    publisher.get_channel().exchange_declare()
    publisher.publish(routing_key='cate.name.action', exchange='pv.asia', body="xXXXx")
