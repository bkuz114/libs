"""
Utility to search through a String (ideally .html or .txt file
that's been read as a String) for delimeters, and places the
text within those delimeters in an HTML tag. e.g., replacing
all instances of {xxx} with <span class="a b c">xxx</span>
"""

import re


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


def wrap_in_tag(string, tag, attrs, pad_left, pad_right):
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
        print("attr: " + attr)
        print("val : " + value)
        wrap += " {}='{}'".format(attr, value)
    wrap += ">" + string + "</" + tag + ">"
    SPACE = "&nbsp;"
    if pad_left:
        wrap = SPACE + wrap
    if pad_right:
        wrap = wrap + SPACE
    return wrap


def template_string(string, delim_open, delim_close, tag, attrs, pad_space):

    # get first char of close delim (need to exclude in regex)
    delim_close_first_char = delim_close[0]
    # escape all three to put in regex
    d_open_esc = escape_string(delim_open)
    d_close_esc = escape_string(delim_close)
    d_close_first_esc = escape_string(delim_close_first_char)

    # setup regexes

    # reg 1: matches all chars between open and close delims,
    # unless that char is the first char of a close delim
    # (essentially like a non-greedy match. Only excluding
    # first char of close delim, as it's too complex to exclude
    # an entire string, end up having to do neg lookahead and
    # it's full of pitfalls -- this is a simple char negation)
    reg_main = '{}([^{}]*){}'.format(
            d_open_esc, d_close_first_esc, d_close_esc)
    # reg 2: same as reg1, but with a space char proceeding
    # and following
    reg_space_both = '(?<=[ ])' + reg_main + '(?=[ ])'
    # reg 3: same as reg 1, but with space char proceeding
    reg_space_left = '(?<=[ ])' + reg_main
    # reg 4: same as reg 1, but with space char following
    reg_space_right = reg_main + '(?=[ ])'

    # Find all desired matches, and replace them.
    if pad_space:
        # order of these regexes important; go from most
        # exclusive to least.
        matches = re.findall(reg_space_both, string)
        for mymatch in matches:
            # remember to not just replace the match --
            # but the delimeters around it (and spaces)
            string = string.replace(
                    " {}{}{} ".format(delim_open, mymatch, delim_close),
                    wrap_in_tag(mymatch, tag, attrs, True, True))
        matches = re.findall(reg_space_left, string)
        for mymatch in matches:
            string = string.replace(
                    " {}{}{}".format(delim_open, mymatch, delim_close),
                    wrap_in_tag(mymatch, tag, attrs, True, False))
        matches = re.findall(reg_space_right, string)
        for mymatch in matches:
            string = string.replace(
                    "{}{}{} ".format(delim_open, mymatch, delim_close),
                    wrap_in_tag(mymatch, tag, attrs, False, True))

    # do the main regex regardless, and if
    # they wanted their tags padded, those are
    # already taken care of, and what remains
    # is matches without anyspace around them
    matches = re.findall(reg_main, string)
    for mymatch in matches:
        string = string.replace(
                "{}{}{}".format(delim_open, mymatch, delim_close),
                wrap_in_tag(mymatch, tag, attrs, False, False))

    return string
