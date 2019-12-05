# coding=utf-8
import argparse
import os
import logging
from logging import config
import settings
from simulator.publisher.message_process import SendingProcess

logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger('main')


def main():
    parser = argparse.ArgumentParser()
    # Create option
    parser.add_argument('-f', '--folder', required=True, help="Folder message")
    parser.add_argument('-p', '--pattern', help="Sending message with routing_key pattern ")
    parser.add_argument('-r', '--routing_key_file', help="Sending message in routing_key_file")

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        parser.error('<folder> incorrect')
    message_process = SendingProcess(routing_key_dir=args.folder)
    LOGGER.info("Starting send message from folder".format(args.folder, ))
    # Run action
    if args.pattern is not None and args.routing_key_file is not None:
        parser.error("you can't choose both pattern and routing_key_file")
    if args.pattern is not None:
        message_process.execute_pattern(args.pattern)
    elif args.routing_key_file is not None:
        message_process.execute(args.routing_key_file)
    else:
        message_process.execute_all()

    return 1


if __name__ == '__main__':
    main()
