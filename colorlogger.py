'''
Sets up root logger of python's logging module
so that it logs to console and a logfile,
and colors console output based on the log level.

usage:

    import utils.colorlogger as colorlogger
    import logging

    colorlogger.setup()
    colorlogger.test()
    logger = logging.getLogger(__name__)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    ** Note: make note of the arguments for 'setup'
    function; depending on arguments given (or not
    given), you will not see all of the test messages
    in the 'usage' above.

'''

import sys
import os
import logging
'''
Need to import io_utils; it's in
same dir as colorlogger, however,
need to add their directory to
path before "import io_utils".
        Why:
if another script is importing
colorlogger and it's in a different
directory than colorlogger, then
'import io_utils' will fail as their
dir is not in the running script's path.
'''
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import io_utils

# some formats to use
FORMAT_LOGFILE = "%(asctime)s:: %(levelname)s: %(message)s (%(filename)s:%(lineno)d)"
FORMAT_CONSOLE_BASIC = "%(message)s"
FORMAT_CONSOLE_HIGH = "%(levelname)s: %(message)s (%(filename)s:%(lineno)d)"

'''
custom logging Formatter to display
log levels in different colors and formatts
https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

NOTE: class name 'CustomFormatter' is not
significant; can make as many of
these classes as I want as long as
they are inheriting from logging.Formatter.
'''


class CustomFormatter(logging.Formatter):

    green = "\x1b[32;20m"
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

    '''
    If a log handler has their
    formatter set to an instance
    of this class, then any
    logging from that handler will
    be filtered through the "format"
    function below: the statement
    being logged will be passed to
    format function; output of that
    function is what gets printed.
    '''
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


'''
set up root logger

Arguments:
    @loglevel_console: (int) level to log onto console
        - valid values are the numeric levels used by
          python's logging module. see:
          https://docs.python.org/3/library/logging.html#logging-levels
    @loglevel_logile: (int) level to log into logfilex
        - valid values are the numeric levels used by
          python's logging module. see:
          https://docs.python.org/3/library/logging.html#logging-levels
    @logfile_nocolor: (String) path of colorless logfile
        - must be absolute path.
        - if None or empty string, won't make one
    @logfile_color: (String) path of colorful logfile
        - must be absolute path.
        - if None or empty string, won't make one
    @console: (boolean) if True, root logger will log to
        console, if False, will NOT log to console.
    @console_nocolor: (boolean) if True, console output
        from root logger will be colorless.
    @stderr: (boolean) if True, then console output from
        from root logger will go to stderr, else will go
        to stdout.
'''


def setup(loglevel_console=logging.DEBUG,
          loglevel_logfile=logging.DEBUG,
          logfile_nocolor=None, logfile_color=None,
          console=True, console_nocolor=False, stderr=False):

    '''
    create handlers (console and logfile(s))
    '''
    handlers = []

    # console handler
    if console:
        mystream = sys.stdout
        if stderr:
            mystream = sys.stderr
        ch = logging.StreamHandler(mystream)
        if console_nocolor:
            ch.setFormatter(logging.Formatter(FORMAT_LOGFILE))
        else:
            ch.setFormatter(CustomFormatter())
        ch.setLevel(loglevel_console)
        handlers.append(ch)
    # regular logfile (prints full date, suppresses color)
    if logfile_nocolor:
        # log file's containing dir must exist or logging will fail
        io_utils.createPath(logfile_nocolor)
        fh = logging.FileHandler(logfile_nocolor, "w")
        fh.setFormatter(logging.Formatter(FORMAT_LOGFILE))
        fh.setLevel(loglevel_logfile)
        handlers.append(fh)
    # colored logfile (same format as console handler; cat to see color)
    if logfile_color:
        # log file's containing dir must exist or logging will fail
        io_utils.createPath(logfile_color)
        fh2 = logging.FileHandler(logfile_color, "w")
        fh2.setFormatter(CustomFormatter())
        fh2.setLevel(loglevel_logfile)
        handlers.append(fh2)

    # set basic configuration for root logger
    '''
    REGARDING SETTING THE LOG LEVEL FOR ROOT LOGGER::

    you MUST set root logger's level, and set it as low as possible.
    Why:
    - if not set, root logger's log level defaults to WARNING.
    - .setLevel() calls on individual handlers are ignored if
      lower than the root logger's
    (e.g. suppose you don't set root loggers level here;
    it will get set to WARNING. Then suppose you set DEBUG
    for a fileHandler's level; since that's lower than WARNING,
    it will get ignored and default to the root logger's level (WARNING)
    so essentially, if you want to set individual log levels on handlers,
    make sure to set root logger's level and set it as low as possible.)
    https://stackoverflow.com/questions/17668633/what-is-the-point-of-setlevel-in-a-python-logging-handler
    '''
    logging.basicConfig(
            level=logging.DEBUG,
            #format='%(asctime)s,%(msecs)d %(levelname)s %(message)s (from file: %(name)s)',
            datefmt='%H:%M:%S',
            handlers=handlers
        )

    if not console and not logfile_color and not logfile_nocolor:
        # disable all logging
        '''
        this next list disabled anything
        from CRITICAL down; hence everything
        '''
        logging.disable(logging.CRITICAL)


def test():
    logger = logging.getLogger(__name__)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
