# coding=utf-8
import os
import re
import logging
from logging import config
import settings
from core.MQ.publisher import Publisher
from simulator.publisher.file_process import *

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


class SendingProcess(object):
    def __init__(self, routing_key_dir,
                 json=BaseJsonProcessing(), xml=BaseXmlProcessing()):
        self.routing_key_dir = routing_key_dir
        self.process = {
            ".json": json.func_process,
            ".xml": xml.func_process,
        }

    def get_name_file(self) -> dict:
        """
        Get name of routing_key
        :return:
        """
        result = {
            '.xml': [],
            '.json': [],
            '.txt': [],
        }
        filenames = os.listdir(self.routing_key_dir)
        for filename in filenames:
            name, file_extension = os.path.splitext(filename)
            if file_extension in result:
                result[file_extension].append(name)
        return result

    def get_content(self, routing_key_path, type) -> list:
        """
        Processing xml, json, txt file to get body,properties,exchange
        :param routing_key:
        :return: list
        """
        return self.process[type](routing_key_path)

    def send(self, routing_key, exchange, body, connection, properties=None):
        """
        Sending message
        :param routing_key:
        :param exchange:
        :param body:
        :param properties:
        :type properties: dict
        :return:
        """

        connection_type = connection['connection_type']
        publisher = Publisher(connection[connection_type])
        publisher.publish(routing_key=routing_key, exchange=exchange, body=body, properties=properties)

    def execute(self, routing_key_file):
        """
        Sending message in a routing_key
        :param routing_key_file:
        :return:
        """
        routing_key_path = os.path.join(self.routing_key_dir, routing_key_file)
        if not os.path.isfile(routing_key_path):
            LOGGER.error('{} not exist'.format(routing_key_file))
            raise FileExistsError
        routing_key, file_type = os.path.splitext(routing_key_file)
        content = self.get_content(routing_key_path, file_type)
        for data in content:
            for exchange in dict(data['exchanges']):
                self.send(routing_key=routing_key, exchange=exchange, connection=data['exchanges'][exchange],
                          body=data['body'],
                          properties=data['properties'])

    def execute_all(self):
        """
        Sending all message
        :return:
        """
        routing_keys = self.get_name_file()
        for file_type in routing_keys:
            for routing_key in routing_keys[file_type]:
                self.execute('{}{}'.format(routing_key, file_type))

    def execute_pattern(self, pattern):
        """
        Sending message have routing_key matched pattern
        :return:
        """
        routing_keys = self.get_name_file()
        for file_type in routing_keys:
            for routing_key in routing_keys[file_type]:
                if re.match(pattern, routing_key):
                    self.execute('{}{}'.format(routing_key, file_type))


if __name__ == '__main__':
    obj = SendingProcess('/vagrant/code/is_mq_manager/simulator/publisher/message_example')
    obj.execute_all()
