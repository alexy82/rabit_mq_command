# coding=utf-8

from settings import SYSTEM_NAME, ENVIRONMENT_NAME


def generate_consumer_tag(exchange: str = None, routing_key: str = None) -> str:
    """
    Generate consumer tag for consumer
    :param exchange: exchange name
    :param routing_key: routing key name
    :param sequence: sequence if exist
    :return:
    """
    host = '{system_name}.{env_name}'.format(
        system_name=SYSTEM_NAME.lower(),
        env_name=ENVIRONMENT_NAME.lower()
    )

    need_join = [host]
    if exchange is None:
        exchange = '__exchange__'
    if routing_key is None:
        routing_key = '__rk__'
    need_join.append(exchange)
    need_join.append(routing_key)

    return '.'.join(need_join)
