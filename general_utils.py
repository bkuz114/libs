""" Useful general utilities that don't fit anywhere else """

import datetime
import re
import os


def absolute(path, relTo):
    """
    Makes a filepath absolute, and normalizes path separators

    :param str path: path to make absolute
    :param str relTo: if path is relative, creates
        the abs path relative to this path.
    :return: str. the normalized, absolute path.
    :example:
        absolute("../b.txt", "C:\\Users\\Boris\\Desktop")
        returns: "C:\\Users\\Boris\\b.txt"
    """
    if not path:
        raise Exception("Path to convert to absolute is "
                        "empty or None.\nPath: {}"
                        .format(path))
    if not os.path.isabs(path):
        if not os.path.isabs(relTo):
            raise Exception("This function takes a path, and "
                            "if that path is not absolute, it "
                            "forms the absolute value of that "
                            "path relative some other path.\n"
                            "Issue: Path passed was not absolute, "
                            "but path to evaluate it from is "
                            "not aboslute either!\n\n"
                            "Path:\n{}\n\n"
                            "Path to evaluate it relative from:\n{}"
                            .format(path, relTo))
        path = os.path.abspath(os.path.join(relTo, path))
    # normpath normalizes in case Unix + Windows separators
    return os.path.normpath(path)


def is_regex_char(string):
    """checks if a string is a reserved regex char"""
    regex_chars = [
            "^", "$", ".", "*", "+", "?", "{", "}",
            "[", "]", "(", ")", "|", "\\"]
    if string in regex_chars:
        return True
    return False


def escape_string(string):
    """escapes regex chars within a string"""
    newstr = ""
    for char in string:
        if is_regex_char(char):
            char = "\\" + char
        newstr += char
    return newstr


def get_filename(file_path, extension=True):
    """get filename from a path with or without extension"""
    basename = os.path.basename(file_path)
    if not extension:
        return os.path.splitext(basename)[0]
    return basename


def file_ext(path):
    """
    return file extension from a path
    :param str path: path to get file ext from
    :return: str. the file extension (if file
        has no extension, returns "")
    :example:
        file_ext("a.txt")
            returns "txt"
        file_ext("b")
            returns ""
    """
    file_ext = os.path.splitext(path)[1]
    # remove . char from extension
    if file_ext:
        return file_ext[1:]
    return ""


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


def wrap_in_tag(string, tag, attrs={}, pad_left=False, pad_right=False):
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
