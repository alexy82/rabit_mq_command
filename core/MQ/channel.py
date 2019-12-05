# coding=utf-8
import pika
from core.MQ.connection import CONNECTION_MANAGER


class ChannelManager(object):
    __channels = {}

    def get_channel(self, obj_info) -> pika.adapters.blocking_connection.BlockingChannel:
        connection_type = obj_info['connection_type']
        channel_name = '{}{}'.format(connection_type, obj_info[connection_type])
        if channel_name in ChannelManager.__channels:
            if ChannelManager.__channels[channel_name].is_open:
                return ChannelManager.__channels[channel_name]

        connection = CONNECTION_MANAGER.get_connection(obj_info[connection_type])
        ChannelManager.__channels[channel_name] = connection.channel()
        return ChannelManager.__channels[channel_name]


CHANNEL_MANAGER = ChannelManager()
