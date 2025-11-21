""" usage: python test_colorlogger.py """

import sys
sys.path.append("..")
import colorlogger as colorlogger  # noqa: E402
import logging  # noqa: E402

colorlogger.setup()

logger = logging.getLogger(__name__)
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
