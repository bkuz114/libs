"""
Test for general_utils.py

usage:
    virtualenv venv && source ./venv/Scripts/activate && pip install -r requirements.txt
    pytest test_general_utils.py [-k 'TEST_A or TEST_B or ... TEST_N']

Examples:

    1. Run all tests
        pytest test_general_utils.py

    2. Run test_get_filename only
        pytest test_general_utils.py -k 'test_get_filename'

    3. Run test_get_filename and test_file_ext
        pytest test_general_utils.py -k 'test_get_filename or test_file_ext'

    4. Run all the 'is_regex_char' tests
        pytest test_general_utils.py -k 'test_is_regex_char'
"""

import sys
sys.path.append("../..")
import general_utils  # noqa: E402


def test_is_regex_char():
    print("Test function: 'is_regex_char', "
          "passing regex chars")

    test_chars = [
            "^", "$", ".", "*", "+", "?", "{", "}",
            "[", "]", "(", ")", "|", "\\"]

    for char in test_chars:
        assert general_utils.is_regex_char(char)


def test_is_regex_char_neg():
    print("Test function: 'is_regex_char', "
          "passing chars that aren't regex chars")

    test_chars = ["a", "not", "&"]

    for char in test_chars:
        assert not general_utils.is_regex_char(char)


def test_escape_string():
    print("Test function 'escape_string'")

    string = "A string with regex ? chars . *, and & non-regex"
    expect = "A string with regex \\? chars \\. \\*, and & non-regex"

    escaped = general_utils.escape_string(string)
    assert escaped == expect


def test_get_filename():
    print("Test function 'get_filename'")

    path = "C:\\Users\\Boris\\myfile.txt"
    expect = "myfile.txt"

    filename = general_utils.get_filename(path)
    assert filename == expect


def test_get_filename_no_ext():
    print("Test function 'get_filename'")

    path = "C:\\Users\\Boris\\myfile"
    expect = "myfile"

    filename = general_utils.get_filename(path)
    assert filename == expect


def test_file_ext():
    print("Test function 'file_ext'")

    path = "C:\\Users\\Boris\\myfile.txt"
    expect = "txt"

    ext = general_utils.file_ext(path)
    assert ext == expect


def test_timestamp():
    print("Test function 'timestamp'")

    timestamp = general_utils.timestamp()
    print("timestamp generated: " + timestamp)
    # ensure no whitespace in the timestamp
    assert " " not in timestamp


def test_wrap_in_tag():
    print("Test function 'wrap_in_tag'")

    string_to_wrap = "Wrap in tag"
    tag = "span"
    attrs = {"lang": "ru", "class": "a b c"}
    expected = '<span lang="ru" class="a b c">{}</span>'.format(string_to_wrap)

    wrap_str = general_utils.wrap_in_tag(
            string_to_wrap, tag, attrs, False, False)
    assert wrap_str == expected


def test_wrap_in_tag_pad():
    print("Test function 'wrap_in_tag', padding with &nbsp;")

    string_to_wrap = "Wrap in tag"
    tag = "span"
    attrs = {"lang": "ru", "class": "a b c"}
    expected = '&nbsp;<span lang="ru" class="a b c">{}' \
               '</span>&nbsp;'.format(string_to_wrap)

    wrap_str = general_utils.wrap_in_tag(
            string_to_wrap, tag, attrs, True, True)
    assert wrap_str == expected
