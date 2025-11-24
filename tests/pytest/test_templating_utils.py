"""
Unit tests for templating_utils.py

usage:
    virtualenv venv && source ./venv/Scripts/activate && pip install -r requirements.txt
    pytest test_templating_utils.py [-k 'TEST_A or TEST_B or ... TEST_N']

Examples:

    1. Run all tests
        pytest test_templating_utils.py

    2. Run test_1 only
        pytest test_templating_utils.py -k 'test_1'

    3. Run test_1 and test_2 only
        pytest test_templating_utils.py -k 'test_1 or test_2'
"""

import sys
sys.path.append("../..")
import templating_utils  # noqa: E402

inner_text1 = "these strings"
inner_text2 = "are in"
inner_text3 = "these"
inner_text4 = "these that are"
LD1 = "{"
RD1 = "}"
LD2 = "["
RD2 = "]"
encapsulated1 = LD1 + inner_text1 + RD1
encapsulated2 = LD1 + inner_text2 + RD1
encapsulated3 = LD2 + inner_text3 + RD2
encapsulated4 = LD2 + inner_text4 + RD2

ORIGINAL = '''
First, I want to template {} that {} curly brackets.
Second, I want to template {} and {} in hard brackets.
'''.format(encapsulated1, encapsulated2, encapsulated3, encapsulated4)


def test_1():
    """test replacing {, } delims with no &nbsp; padding"""
    print("\nTest #1: Template {}, {} delims (no &nbsp; padding)".format(
        LD1, RD1))
    print("Original:")
    print(ORIGINAL)
    classes_to_add = "a b c"
    templated = templating_utils.template_string(
        ORIGINAL, LD1, RD1, "span",
        {"class": classes_to_add}, False)
    print("Templated:")
    print(templated)
    expected_tag1 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text1)
    expected = ORIGINAL.replace(encapsulated1, expected_tag1)
    expected_tag2 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text2)
    expected = expected.replace(encapsulated2, expected_tag2)
    assert templated == expected


def test_2():
    """test replacing [, ] delims with no &nbsp; padding"""
    print("\nTest #2: Template {}, {} delims (no &nbsp; padding)".format(
        LD2, RD2))
    print("Original:")
    print(ORIGINAL)
    classes_to_add = "a b c"
    templated = templating_utils.template_string(
        ORIGINAL, LD2, RD2, "span",
        {"class": classes_to_add}, False)
    print("Templated:")
    print(templated)
    expected_tag1 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text3)
    expected = ORIGINAL.replace(encapsulated3, expected_tag1)
    expected_tag2 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text4)
    expected = expected.replace(encapsulated4, expected_tag2)
    assert templated == expected


def test_3():
    """test replacing {, } delims with &nbsp; padding"""
    print("\nTest #1: Template {}, {} delims (&nbsp; padding)".format(
        LD1, RD1))
    print("Original:")
    print(ORIGINAL)
    classes_to_add = "a b c"
    templated = templating_utils.template_string(
        ORIGINAL, LD1, RD1, "span",
        {"class": classes_to_add}, True)
    print("Templated:")
    print(templated)
    expected_tag1 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text1)
    expected = ORIGINAL.replace(encapsulated1, expected_tag1)
    expected_tag2 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text2)
    expected = expected.replace(encapsulated2, expected_tag2)
    expected = expected.replace(" <span", "&nbsp;<span")
    expected = expected.replace("</span> ", "</span>&nbsp;")
    assert templated == expected


def test_4():
    """test replacing [, ] delims with &nbsp; padding"""
    print("\nTest #4: Template {}, {} delims (&nbsp; padding)".format(
        LD2, RD2))
    print("Original:")
    print(ORIGINAL)
    classes_to_add = "a b c"
    templated = templating_utils.template_string(
        ORIGINAL, LD2, RD2, "span",
        {"class": classes_to_add}, True)
    print("Templated:")
    print(templated)
    expected_tag1 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text3)
    expected = ORIGINAL.replace(encapsulated3, expected_tag1)
    expected_tag2 = '<span class="{}">{}</span>'.format(
            classes_to_add, inner_text4)
    expected = expected.replace(encapsulated4, expected_tag2)
    expected = expected.replace(" <span", "&nbsp;<span")
    expected = expected.replace("</span> ", "</span>&nbsp;")
    assert templated == expected
