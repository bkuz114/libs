import datetime
import re


def timestamp():
    """Generate timestamp string with no spaces"""
    # format the datetime without any spaces
    fmt = "%Y_%m_%d-%H_%M_%S"
    ct = datetime.datetime.now().strftime(fmt)
    return str(ct)


def urlify(s):
    """remove chars from string that will cause issues in an URL"""

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s
