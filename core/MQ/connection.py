# coding=utf-8
import time
import hashlib
import pika
import logging
from logging import config
import settings
from core.utils.helpers import import_class_by_path

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')

AMQP_URL_FIELD_NAME = 'AMQP_URL'


class BlockingConnection(object):
    """Connection class of AMQP"""

    __connection = None
    __max_attempt_retry = 3

    def __init__(self, uri: str = None, host: str = None, port: int = 5672, vhost: str = None,
                 user: str = None, password: str = None, **options):
        if uri is not None:
            self.__parameters = pika.URLParameters(uri)
        else:
            credentials = pika.PlainCredentials(username=user, password=password)
            self.__parameters = pika.ConnectionParameters(host=host, port=port, virtual_host=vhost,
                                                          credentials=credentials, **options)
        if options.get('max_attempt_retry') is not None:
            self.__max_attempt_retry = max(self.__max_attempt_retry, 0)

    def connect(self, attempts_retry: int = None) -> pika.BlockingConnection:
        """
        Connect to message broker and return connection
        :param attempts_retry:
        :return:
        """
        if attempts_retry is None:
            attempts_retry = self.__max_attempt_retry
        else:
            attempts_retry = min(attempts_retry, self.__max_attempt_retry)
        attempts = 0
        while True:
            attempts += 1
            try:
                self.__connection = pika.BlockingConnection(parameters=self.__parameters)
                LOGGER.info('Connected: {attempts} | {host}:{port}/{vhost}'.format(
                    attempts=attempts,
                    host=self.__parameters.host,
                    port=self.__parameters.port,
                    vhost=self.__parameters.virtual_host
                ))
                break
            except:
                LOGGER.warning('Retry connect: {attempts} | {host}:{port}/{vhost}'.format(
                    attempts=attempts,
                    host=self.__parameters.host,
                    port=self.__parameters.port,
                    vhost=self.__parameters.virtual_host
                ))
                if attempts > attempts_retry:
                    LOGGER.exception(
                        'Cannot connect to queue {host}:{port}/{vhost} after {attempts}'.format(
                            attempts=attempts,
                            host=self.__parameters.host,
                            port=self.__parameters.port,
                            vhost=self.__parameters.virtual_host
                        ))
                    break
                time.sleep(min(attempts * 2, 30))
        return self.__connection


class Connections(object):
    """Connections Manager"""

    def __init__(self, configs=None):
        self.configs = configs
        self.connections = {}

    def get_connection(self, name_conn: str):
        '''

        :param type: 'settings' or 'url'
        :param content: if type is 'settings' content will be a connection's name  in settings,
                        if type is 'url' content will be a connection's url
        :return:
        '''
        name = hashlib.md5(name_conn.encode('utf-8')).hexdigest()

        if name in self.connections and self.connections[name].is_open:
            return self.connections[name]
        if name_conn.startswith('amqp://'):
            self.connections[name] = pika.BlockingConnection(pika.URLParameters(name_conn))
            return self.connections[name]
        if name_conn not in self.configs:
            return None

        config = self.configs.get(name_conn, {})
        options = config.get('OPTIONS', {})
        cls_name = import_class_by_path(config.get('CLS', 'BlockingConnection'))
        self.connections[name] = cls_name(
            uri=config.get(AMQP_URL_FIELD_NAME, None),
            host=config.get('HOST', None),
            port=config.get('PORT', None),
            vhost=config.get('VHOST', None),
            user=config.get('USER', None),
            password=config.get('PASSWORD', None),
            **options
        ).connect(options.get('MAX_ATTEMPTS_RETRY', None))
        return self.connections[name]

    def connect_all(self):
        for name, config in self.configs:
            self.get_connection(name)

    def get_connections(self) -> dict:
        self.connect_all()
        return self.connections


CONNECTION_MANAGER = Connections(settings.AMQP)
