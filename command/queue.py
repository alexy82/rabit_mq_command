# coding=utf-8
import argparse
import json
import logging
from logging import config
import settings
from core.MQ.queue_helper import QueueHelper

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


def main():
    parser = argparse.ArgumentParser()
    # Create option
    parser.add_argument('action', choices=['remove', 'declare', 'bind'], help='Action process queues')
    parser.add_argument('-f', '--file', required=True, help='file json config queues')
    parser.add_argument('-p', '--pattern', help="Pattern queue")
    parser.add_argument('-q', '--queue', help="Specify exchange")
    parser.add_argument('-e', '--empty', action='store_true',
                        help="Remove if queue doesn't have messgae \n use with action remove",
                        default=False)
    parser.add_argument('-u', '--unused', action='store_true',
                        help="Remove if no consumer connect queue \n use with action remove ",
                        default=False)

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

    qu_helper = QueueHelper(data['declare'], data['bind'])
    # Check legal input
    if args.pattern is not None and args.queue is not None:
        parser.error('you must choose one in <pattern> and <queue>')
    if args.action != 'remove' and (args.unused or args.empty):
        parser.error('you only use <unused> and <empty>  with action remove')

    # Call action
    LOGGER.info(
        "Starting {} queues from file {}".format(args.action, args.file))
    if args.queue is not None:
        if (args.action == 'remove'):
            qu_helper.action[args.action](args.queue, if_unused=args.unused, if_empty=args.empty)
        else:
            qu_helper.action[args.action](args.queue)
    elif args.pattern is not None:
        if (args.action == 'remove'):
            qu_helper.action[args.action](args.pattern, if_unused=args.unused, if_empty=args.empty)
        else:
            qu_helper.action_pattern[args.action](args.pattern)
    else:
        qu_helper.action_all[args.action]()

    return 1


if __name__ == '__main__':
    main()
