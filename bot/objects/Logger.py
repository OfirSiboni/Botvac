import logging


class Logger:
    def __init__(self):
        logging.basicConfig(format="%(time)s|%(levelname)s| (%message)s")

    def info(self, msg: str):
        print(msg)
        logging.info(msg)

    def debug(self, msg: str):
        print(msg)
        logging.debug(msg)

    def warning(self, msg: str):
        print(msg)
        logging.warning(msg)

    def error(self, msg):
        print(msg)
        logging.error(msg)

    def exception(self, msg):
        print(msg)
        logging.exception(msg)
