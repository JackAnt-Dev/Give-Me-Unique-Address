import logging
from logging import getLogger
from logging.handlers import SysLogHandler
from logging import FileHandler, StreamHandler, Formatter
import os
import sys
import time

from typing import Callable

DEFAULT_LOG_ADDRESS = ''      # host:port
DEFAULT_LOG_PERIOD = '1000'  # positive integer
DEFAULT_LOG_LEVEL = 'DEBUG'  # DEBUG/INFO/WARNING/ERROR/CRITICAL

DEFAULT_LOG_NAME = 'basic'

WRITE_TO_CONSOLE = True

WRITE_TO_FILE = True                    # write to file if this is true

DEFAULT_FILE_BASE = "../../logs"  # relative dir to this file
DEFAULT_FILE_NAME = f"log_{int(time.time())}.txt"


def simple_logger(name, console=True, filepath=None):
    # make simple logger
    mylogger = logging.getLogger(name)
    mylogger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        mylogger.addHandler(stream_handler)

    if filepath:
        # clear log file existed
        with open(filepath, 'wt') as f:
            pass
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(formatter)
        mylogger.addHandler(file_handler)

    return mylogger


class Logger(object):
    def __init__(self, name, console=True, filepath=None):
        self.logger = getLogger(name)
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.period = int(os.getenv('LOG_PERIOD', DEFAULT_LOG_PERIOD))
        level = getattr(logging, os.getenv(
            'LOG_LEVEL', DEFAULT_LOG_LEVEL).upper())
        address = os.getenv('LOG_ADDRESS', DEFAULT_LOG_ADDRESS)
        if address:
            host, port = address.split(':')
            file_name = os.path.basename(sys.argv[0])
            log_message = Formatter(file_name+' %(message)s')
            syslogHandler = SysLogHandler(address=(host, int(port)))
            syslogHandler.setFormatter(log_message)
            self.logger.addHandler(syslogHandler)

        basic_message = Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if console:
            streamHandler = StreamHandler(sys.stdout)
            streamHandler.setFormatter(basic_message)
            self.logger.addHandler(streamHandler)

        if filepath:
            # clear log file existed
            with open(filepath, 'wt') as f:
                pass
            file_handler = FileHandler(filepath)
            file_handler.setFormatter(basic_message)
            self.logger.addHandler(file_handler)

        self.logger.setLevel(level)

    def periodic(self, testCount, numOfTests, message):
        func = self.debug if testCount % self.period else self.info
        func('Test {} out of {}: {}'.format(testCount, numOfTests, message))

    def change_path(self, new_path):
        # remove existing file handlers
        fhdrls = [hdrl for hdrl in self.logger.handlers if isinstance(
            hdrl, FileHandler)]
        if not fhdrls:
            self.logger.warning('no file handler.')
            return
        formatter = fhdrls[0].formatter
        # clear log file existed
        with open(new_path, 'wt') as f:
            pass
        for hdrl in fhdrls:
            self.logger.removeHandler(hdrl)
        # add new file handler
        new_handler = FileHandler(new_path)
        new_handler.setFormatter(formatter)
        self.logger.addHandler(new_handler)


if WRITE_TO_FILE:
    base = os.path.realpath(os.path.join(__file__, DEFAULT_FILE_BASE))
    if not os.path.exists(base):
        os.makedirs(base)

default_file_path = \
    os.path.realpath(
        os.path.join(__file__, DEFAULT_FILE_BASE, DEFAULT_FILE_NAME)) if WRITE_TO_FILE else None

logger = Logger(DEFAULT_LOG_NAME, console=WRITE_TO_CONSOLE,
                filepath=default_file_path)


def checkpoint(f: Callable):
    # helper: timing function
    def _innermost_func(f: Callable):
        if f.__closure__ is not None:
            return _innermost_func(f.__closure__[0].cell_contents)
        else:
            return f

    def wrapper(*args, **kwargs):
        f_im = _innermost_func(f)
        logger.info(f"======== start of {f_im.__name__}() ========")
        output = f(*args, **kwargs)
        # if output:
        #     logger.info(output)
        logger.info(f"======== end of {f_im.__name__}() ========")
        return output
    return wrapper


# logger = simple_logger('metaplex', console=True, filepath='log.txt')

if __name__ == '__main__':
    import os
    logpath = os.path.abspath(os.path.join(
        __file__, "..", "..", "logs", "log.txt"))
    logger.change_path(logpath)
    logger.info("testestestest")
