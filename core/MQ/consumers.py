# coding=utf-8
import pika
import logging
from logging import config
import settings
from core.MQ.connection import CONNECTION_MANAGER

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


class BaseConsumer(object):
    """Base class for consumer"""
    channel = None
    connection_name = None

    def __init__(self, queue_name: str, connection_name: str):
        """
        Constructor for Basic Consumer
        :param queue_name: queue name
        :param binding_dict: dictionary, key
        :param queue_options: options for queue
        :param connection: connection key in settings
        """

        self.queue_name = queue_name
        self.connection_name = connection_name
        self.connection = CONNECTION_MANAGER.get_connection(connection_name)

    def get_channel(self):
        """
        Get channel of this consumer
        :return:
        """
        if self.channel is None or not self.channel.is_open:
            if not self.connection.is_open:
                self.connection = CONNECTION_MANAGER.get_connection(self.connection_name)
            self.channel = self.connection.channel()
        return self.channel

    def start(self):
        """
        Start consuming
        :return:
        """
        try:
            self.active = True
            self.channel = self.get_channel()
            self.channel.basic_consume(self.message_process, queue=self.queue_name, no_ack=False)

            LOGGER.info('Start consuming queue {queue}'.format(queue=self.queue_name))
            self.channel.start_consuming()
        except:
            LOGGER.exception(
                'Failed to start connection {connection_name} | queue {queue_name}'.format(
                    connection_name=self.connection_name,
                    queue_name=self.queue_name
                ))
        finally:
            LOGGER.info('Stop consuming queue {queue}'.format(queue=self.queue_name))
            self.active = False

    def stop(self):
        """
        Stop consuming
        :return:
        """
        self.channel.stop_consuming()

    def message_process(self, channel: pika.adapters.blocking_connection.BlockingChannel,
                        method_frame, header_frame, body):
        """
        Process message. Can be overrode in sub classes
        :param channel:
        :param method_frame:
        :param header_frame:
        :param body:
        :return:
        """
        LOGGER.info('routing key: {routing_key} | headers: {headers} | body: {body}'.format(
            routing_key=method_frame.routing_key,
            headers=header_frame.headers,
            body=body.decode(),
        ))
        channel.basic_ack(method_frame.delivery_tag)
        # channel.basic_nack(delivery_tag=method_frame.delivery_tag, multiple=False, requeue=True)



if __name__ == '__main__':
    consumer = BaseConsumer(queue_name='test',connection_name='amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf')
    consumer.start()
