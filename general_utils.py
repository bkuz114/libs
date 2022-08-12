import datetime
import re

'''
Generate a timestamp string with no spaces
'''
def timestamp():
    # format the datetime without any spaces
    fmt = "%Y_%m_%d-%H_%M_%S"
    ct = datetime.datetime.now().strftime(fmt)
    return str(ct)

'''
take a string and make to be used in an URL
(remove chars that will cause a problem)
'''
def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s


