"""
Utility to search through a String (ideally .html or .txt file
that's been read as a String) for delimeters, and places the
text within those delimeters in an HTML tag. e.g., replacing
all instances of {xxx} with <span class="a b c">xxx</span>
"""

import re
import general_utils


def template_string(string, delim_open, delim_close, tag, attrs, pad_space):

    # get first char of close delim (need to exclude in regex)
    delim_close_first_char = delim_close[0]
    # escape all three to put in regex
    d_open_esc = general_utils.escape_string(delim_open)
    d_close_esc = general_utils.escape_string(delim_close)
    d_close_first_esc = general_utils.escape_string(delim_close_first_char)

    # setup regexes

    # reg 1: matches all chars between open and close delim
    # unless that char is the 1st char of the close delim.
    # This is essentially like a non-greedy match, where the
    # reg will stop once it hits the first close char it
    # encounters. Doing it this way rather than a basic
    # non-greedy match, as will be building on this regex
    # to look for optional spaces around it, and the non-greedy
    # won't work in those situations, but this does.
    # Note: only excluding first char of close delim -- rather
    # than the entire close delim -- as it's too complex to
    # exclude an entire string (which you would need to do if
    # the close delim is more than one char). You end up having to
    # do neg lookahead if you want to exclude the entire close
    # delim and it's full of pitfalls --
    # this is a simple char negation and it still works.
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
                    general_utils.wrap_in_tag(
                        mymatch, tag, attrs, True, True))
        matches = re.findall(reg_space_left, string)
        for mymatch in matches:
            string = string.replace(
                    " {}{}{}".format(delim_open, mymatch, delim_close),
                    general_utils.wrap_in_tag(
                        mymatch, tag, attrs, True, False))
        matches = re.findall(reg_space_right, string)
        for mymatch in matches:
            string = string.replace(
                    "{}{}{} ".format(delim_open, mymatch, delim_close),
                    general_utils.wrap_in_tag(
                        mymatch, tag, attrs, False, True))

    # do the main regex regardless, and if
    # they wanted their tags padded, those are
    # already taken care of, and what remains
    # is matches without anyspace around them
    matches = re.findall(reg_main, string)
    for mymatch in matches:
        string = string.replace(
                "{}{}{}".format(delim_open, mymatch, delim_close),
                general_utils.wrap_in_tag(mymatch, tag, attrs, False, False))

    return string
