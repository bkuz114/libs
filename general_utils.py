import datetime
import re


def escape_string(string):
    """escapes regex chars within a string"""
    newstr = ""
    for char in string:
        if is_regex_char(char):
            char = "\\" + char
        newstr += char
    return newstr


def is_regex_char(string):
    """checks if a string is a reserved regex char"""
    regex_chars = [
            "^", "$", ".", "*", "+", "?", "{", "}",
            "[", "]", "(", ")", "|", "\\"]
    if string in regex_chars:
        return True
    return False


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


def wrap_in_tag(string, tag, attrs, pad_left=False, pad_right=False):
    """
    wrap a string in an HTML tag with given attrs, and
    optionally pad with &nbsp; chars on either side.
    example:
        wrap_in_tag("hello", "span", {{"class": "a b c"}}
    returns
        "<span class="a b c">hello</span>"

    :param String string: string to put in a tag
    :param String tag: tag to wrap in (i.e. "span", "div")
    :param dict<String, String> attrs: HTML attrs to
        add to the tag
    :param boolean pad_left: if True, add &nbsp; to left
        of tag (useful if tag="span", and the <span> will
        be direct child of a <p> with font-size=0, which is
        a strategy to remove default padding around <span>s.
        Such a strategy will remove ALL <span> padding,
        so even if you have a space char prior to the <span>,
        it won't render, and will need a &nbsp; to render
        a space)
    :param boolean pad_right: if True, add &nbsp; to right
        of tag (see comment for pad_left on usefulness)
    :return String: the string wrapped in the tag
    """
    wrap = "<" + tag
    for attr, value in attrs.items():
        wrap += ' {}="{}"'.format(attr, value)
    wrap += ">" + string + "</" + tag + ">"
    SPACE = "&nbsp;"
    if pad_left:
        wrap = SPACE + wrap
    if pad_right:
        wrap = wrap + SPACE
    return wrap
