'''
Sets up root logger of python's logging module
so that it logs to console and a logfile,
and colors console output based on the log level.

usage:

    import utils.colorlogger as colorLogger

    colorLogger.setup()
    colorLogger.test()

'''

import sys
import logging
import io_utils

# some formats to use
FORMAT_LOGFILE = "%(asctime)s:: %(levelname)s: %(message)s (%(filename)s:%(lineno)d)"
FORMAT_CONSOLE_BASIC = "%(message)s"
FORMAT_CONSOLE_HIGH = "%(levelname)s: %(message)s (%(filename)s:%(lineno)d)"

'''
custom logging Formatter to display
log levels in different colors and formatts
https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
'''
class CustomFormatter(logging.Formatter):

    green ="\x1b[32;20m"
    blue = "\x1b[34;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: green + FORMAT_CONSOLE_BASIC + reset,
        logging.INFO: blue + FORMAT_CONSOLE_BASIC + reset,
        logging.WARNING: yellow + FORMAT_CONSOLE_HIGH + reset,
        logging.ERROR: red + FORMAT_CONSOLE_HIGH + reset,
        logging.CRITICAL: bold_red + FORMAT_CONSOLE_HIGH + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

'''
set up root logger

Arguments:
    @loglevel: what level to log from
    @logfile_nocolor: path of colorless logfile
        (rel script importing this; if none, don't make one.)
    @logfile_color: path of colorful logfile
        ("" "")
'''
def setup(loglevel_console=logging.DEBUG, loglevel_logfile=logging.DEBUG, logfile_nocolor=None, logfile_color=None):
    '''
    create handlers (console and logfile)
    '''
    handlers = []

    # console handler
    ch = logging.StreamHandler(sys.stdout) # if you don't do this, will print to stderr
    ch.setFormatter(CustomFormatter())
    ch.setLevel(loglevel_console)
    handlers.append(ch)

    # logfile handlers
    # first logfile (prints full date, suppresses color)
    if logfile_nocolor:
        io_utils.createPath(logfile_nocolor) # parent dir must exist of logging will fail
        fh = logging.FileHandler(logfile_nocolor, "w")
        fh.setFormatter(logging.Formatter(FORMAT_LOGFILE))
        fh.setLevel(loglevel_logfile)
        handlers.append(fh)
    # second logfile (same format as console handler; cat to see the color)
    if logfile_color:
        io_utils.createPath(logfile_color)
        fh2 = logging.FileHandler(logfile_color, "w")
        fh2.setFormatter(CustomFormatter())
        fh2.setLevel(loglevel_logfile)
        handlers.append(fh2)

    # set basic configuration for root logger
    logging.basicConfig(
            '''
            REGARDING SETTING THE LOG LEVEL FOR ROOT LOGGER::

            you MUST set root logger's level, and set it as low as possible. Why:
            - if not set, root logger's log level defaults to WARNING.
            - .setLevel() calls on individual handlers are ignored if lower than the root logger's
            (e.g. suppose you don't set root loggers level here;
            it will get set to WARNING. Then suppose you set DEBUG
            for a fileHandler's level; since that's lower than WARNING,
            it will get ignored and default to the root logger's level (WARNING)
            so essentially, if you want to set individual log levels on handlers,
            make sure to set root logger's level and set it as low as possible.)
            https://stackoverflow.com/questions/17668633/what-is-the-point-of-setlevel-in-a-python-logging-handler
            '''
            level=logging.DEBUG,
            #format='%(asctime)s,%(msecs)d %(levelname)s %(message)s (from file: %(name)s)',
            datefmt='%H:%M:%S',
            handlers=handlers
        )

def test():
    logger = logging.getLogger(__name__)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
