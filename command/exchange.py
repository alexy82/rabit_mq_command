# coding=utf-8
import argparse
import json
import logging
from logging import config
import settings
from core.MQ.exchange_helper import ExchangeHelper

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


def main():
    parser = argparse.ArgumentParser()
    # Create option
    parser.add_argument('action', choices=['remove', 'declare', 'bind'], help='Action process exchanges')
    parser.add_argument('-f', '--file', action='store', required=True, help='file json config exchange')
    parser.add_argument('-e', '--exchange', help='specify exchange')

    args = parser.parse_args()
    try:
        with open(args.file) as f:
            data = json.load(f)
        for key in ["declare", "bind"]:
            if key not in data:
                raise AttributeError
    except:
        LOGGER.exception('incorrect file')
        parser.error("Incorrect file")

    exchange_helper = ExchangeHelper(data['declare'], data['bind'])
    LOGGER.info(
        "Starting {} {} exchange from file {}".format(args.action, "all" if args.exchange is None else args.exchange,
                                                      args.file))
    if args.exchange is None:
        exchange_helper.action_all[args.action]()
    else:
        exchange_helper.action[args.action](args.exchange)
        bool()


    return 1


if __name__ == '__main__':
    main()
