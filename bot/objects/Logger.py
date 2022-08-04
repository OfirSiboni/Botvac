import logging


class Logger:
    def __init__(self):
        logging.basicConfig(format="%(time)s|%(levelname)s| (%message)s")

    def info(self, msg: str):
        logging.info(msg)

    def debug(self, msg: str):
        logging.debug(msg)

    def warning(self, msg: str):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def exception(self, msg):
        logging.exception(msg)
