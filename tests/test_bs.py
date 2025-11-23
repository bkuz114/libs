"""
unit tests for beautiful_soup_utils.py

run with pytest:

    virtualenv tests && source ./tests/Scripts/activate && pip install -r ../requirements.txt
    pytest test_bs.py

    -- will run ALL functions prefixed with test_
    -- requirements.txt will install pytest

run a specific test (example: run test_add_classes):

    virtualenv tests && source ./tests/Scripts/activate && pip install -r ../requirements.txt
    pytest test_bs.py -k 'test_add_classes or test_add_css_head_tags or test_has_text_content'

run multiple specific test (example: run test_add_classes, test_add_css_head_tags and test_has_text_content):

    virtualenv tests && source ./tests/Scripts/activate && pip install -r ../requirements.txt
    pytest test_bs.py -k 'test_add_classes or test_add_css_head_tags or test_has_text_content'


IMPORTANT:
    Use pytest rather than built in python unittest, as many
    assert list1 == list2, and I believe pytest has different
    functionality in determining list equality that unittest
    does not.

Note: to include print statements on console output, add -s flag

If do NOT want to run with pytest, can call with python, and it will
run all functions prefixed with test_

    virtualenv tests && source ./tests/Scripts/activate && pip install -r ../requirements.txt
    python test_bs.py
"""

import inspect
import sys
import os
import datetime
import re
from bs4 import BeautifulSoup
sys.path.append("..")
import beautiful_soup_utils  # noqa: E402

# to create a timestampped output dir
# (used by the test_write_ unit tests)
script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir_base = os.path.join(script_dir, "output_test_bs")
fmt = "%Y_%m_%d-%H_%M_%S"
ct = datetime.datetime.now().strftime(fmt)
OUTPUT_DIR = os.path.abspath(os.path.join(output_dir_base, ct))


def test_add_classes():
    """ test add_classes functions """

    soup = BeautifulSoup("", 'html.parser')
    h1 = soup.new_tag("h1")
    expected_classes = []
    classes = beautiful_soup_utils.get_classes(h1)
    assert classes == expected_classes
    beautiful_soup_utils.add_classes(h1, ["hello", "me"])
    beautiful_soup_utils.add_classes(h1, ["more", "stuff"])
    beautiful_soup_utils.add_classes(h1, ["more", "stuff"])
    expected_classes = ["hello", "me", "more", "stuff"]
    classes = beautiful_soup_utils.get_classes(h1)
    assert classes == expected_classes
    print("pass")


def test_find_replace():
    """ test find_replace_str functions """

    soup = BeautifulSoup("<p>Hello World</p>", 'html.parser')
    print("soup before:\n\t" + str(soup))
    search_for1 = "Hello"
    search_for2 = "World"
    replace_with1 = "Goodbye :("
    replace_with2 = "Sweet, Sweet Earth"
    assert search_for1 in str(soup)
    assert search_for2 in str(soup)
    assert replace_with1 not in str(soup)
    assert replace_with2 not in str(soup)
    print("Replace " + search_for1 + " with " + replace_with1)
    beautiful_soup_utils.find_replace_str(soup, search_for1, replace_with1)
    print("Replace " + search_for2 + " with " + replace_with2)
    beautiful_soup_utils.find_replace_str(soup, search_for2, replace_with2)
    print("after:\n\t" + str(soup))
    assert replace_with1 in str(soup)
    assert replace_with2 in str(soup)
    assert search_for1 not in str(soup)
    assert search_for2 not in str(soup)
    # replace a string with a tag
    search_for3 = "Goodbye"
    html_str = "<h1>stuff</h1>"
    soup_tag = BeautifulSoup(html_str)
    print("Replace " + search_for3 + " with a tag: " + str(soup_tag))
    beautiful_soup_utils.find_replace_str(soup, search_for3, soup_tag)
    print("after:\n\t" + str(soup))
    assert html_str in str(soup)
    assert search_for3 not in str(soup)
    print("pass")


def test_css_classes():
    """ test add_classes and get_classes functions """

    soup = BeautifulSoup("", 'html.parser')
    h1 = soup.new_tag("h1")
    expected_classes = []
    classes = beautiful_soup_utils.get_classes(h1)
    assert classes == expected_classes
    classes = beautiful_soup_utils.get_classes(h1)
    classes_to_add = ["mmmm", "here2", "here5"]
    beautiful_soup_utils.add_classes(h1, classes_to_add)
    expected_classes = classes_to_add
    classes = beautiful_soup_utils.get_classes(h1)
    assert classes == expected_classes
    classes_to_remove = ["mmmm", "here2", "h343", "here1"]
    beautiful_soup_utils.remove_classes(h1, classes_to_remove)
    expected_classes = list(set(classes_to_add) - set(classes_to_remove))
    classes = beautiful_soup_utils.get_classes(h1)
    assert classes == expected_classes
    print("pass")


def test_get_css_head_tags():
    """ test get_css_head_tags function """

    html_str1 = "<html><head></head><body></body></html>"
    soup = BeautifulSoup(html_str1, 'html.parser')
    print("soup to get head tags from: " + html_str1)
    expected_tags = []
    tags = beautiful_soup_utils.get_css_head_tags(soup)
    assert tags == expected_tags
    link_str1 = '<link href="dummytag.css" rel="stylesheet" type="text/css">'
    link_str2 = '<link href="dummytag2.css" rel="stylesheet" type="text/css">'
    html_str2 = "<html><head>" + link_str1 + link_str2 + "</head><body></body></html>"
    soup = BeautifulSoup(html_str2, 'html.parser')
    print("soup to get head tags from: " + html_str2)
    expected_tags = [link_str1, link_str2]
    tags = beautiful_soup_utils.get_css_head_tags(soup)
    # the tags will have trailing slashes (i.e. <link ... />
    # -- all beautifulsoup parsers will add those
    # to remove (so that you can accurately assert:
    #  1. encode the tag with html5 formatter
    #     (removes trailing slashes, but returns a bytes literal)
    #  2. decode bytes literal to string
    str_tags = [(x.encode(formatter="html5").decode("utf-8")) for x in tags]
    print("<link> tags found:")
    for tag in str_tags:
        print(tag)
    assert str_tags == expected_tags


def insert_at(a, b, pos):
    """
    merge two lists at a specific position
        a = [1, 2, 3]
        b = [4, 5, 6]
    insert_at(a, b, 1)
        [1, 4, 5, 6, 2, 3]
    """
    return a[0:pos] + b + a[pos:]


def test_add_css_head_tags():
    """ test add_css_head_tags function """

    html_str1 = "<html><head></head><body></body></html>"
    soup = BeautifulSoup(html_str1, 'html.parser')
    expected_tags = []
    tags = beautiful_soup_utils.get_css_head_tags(soup)
    assert expected_tags == tags

    paths = ["dummy1.css", "dummy2.css"]
    print("add css head tags: " + str(paths) +
          " (appends to END of <head> by default)")
    beautiful_soup_utils.add_css_head_tags(soup, paths)
    print("Result:")
    print(soup.prettify(formatter="html5"))
    expected_tags = paths
    tags = [x["href"] for x in beautiful_soup_utils.get_css_head_tags(soup)]
    assert expected_tags == tags

    paths2 = ["dummy-ind1.css", "./assets/dummy-ind2.css"]
    print("add css head tags: " + str(paths2) + " at index 0")
    beautiful_soup_utils.add_css_head_tags(soup, paths2, startAt=0)
    print("Result:")
    print(soup.prettify(formatter="html5"))
    expected_tags = insert_at(paths, paths2, 0)
    tags = [x["href"] for x in beautiful_soup_utils.get_css_head_tags(soup)]
    assert expected_tags == tags

    paths3 = ["dummy-ind-mid1.css", "/here/dummy-ind-mid2.css"]
    print("add css head tags: " + str(paths3) + " at index 3")
    beautiful_soup_utils.add_css_head_tags(soup, paths3, startAt=3)
    print("Result:")
    print(soup.prettify(formatter="html5"))
    expected_tags = insert_at(expected_tags, paths3, 3)
    tags = [x["href"] for x in beautiful_soup_utils.get_css_head_tags(soup)]
    assert expected_tags == tags
    print("pass")


def test_update_tag_paths():
    """ update update_paths function """

    html_str1 = "<html><head></head><body></body></html>"
    print("generate basic HTML document...")
    soup = BeautifulSoup(html_str1, 'html.parser')
    expected_tags = []
    tags = beautiful_soup_utils.get_css_head_tags(soup)
    assert expected_tags == tags

    paths = ["dummy-ind1.css", "./assets/dummy-ind2.css"]
    print("add css head tags to document: " + str(paths))
    beautiful_soup_utils.add_css_head_tags(soup, paths, startAt=0)
    expected_tag_hrefs = paths
    tag_hrefs = [
            x["href"] for x in beautiful_soup_utils.get_css_head_tags(soup)]
    assert expected_tag_hrefs == tag_hrefs

    # update paths in head tags
    rel = "../.."
    print("Update the head tags to be relative to " + rel)
    # print("soup before:")
    # print(soup.prettify(formatter="html5"))
    beautiful_soup_utils.update_paths(soup, rel)
    # print("soup after:")
    # print(soup.prettify(formatter="html5"))
    expected_tag_hrefs = [os.path.normpath(rel + x) for x in paths]
    tag_hrefs = [
            x["href"] for x in beautiful_soup_utils.get_css_head_tags(soup)]
    assert expected_tag_hrefs == tag_hrefs
    print("pass")


def test_remove_non_internal_comments():
    """
    test remove_html_comments function,
    with option to keep comments inserted
    internally by beautiful_soup_utils
    """

    added_comment = "<!-- a comment -->"
    html_str = '''
<html>
    <head></head>
    {}
    <body>
    </body>
</html>'''.format(added_comment)
    print("general basic beautifulsoup with one comment")
    soup = BeautifulSoup(html_str, 'html.parser')
    assert added_comment in str(soup)
    assert beautiful_soup_utils.LINK_COMMENT not in str(soup)

    print("add css tags so that an internal comment is added")
    beautiful_soup_utils.add_css_head_tags(soup, ["dummytag.css"])
    # make sure the internal comment is now there
    assert beautiful_soup_utils.LINK_COMMENT in str(soup)

    print("call remove_html_comnents, with option to "
          "preserve internally added comments")
    beautiful_soup_utils.remove_html_comments(soup, True)

    assert added_comment not in str(soup)
    assert beautiful_soup_utils.LINK_COMMENT in str(soup)


def test_remove_all_comments():
    """
    test remove_html_comments function,
    with option to remove all comments
    """

    added_comment = "<!-- a comment -->"
    html_str = '''
<html>
    <head></head>
    {}
    <body>
    </body>
</html>'''.format(added_comment)
    print("general basic beautifulsoup with one comment")
    soup = BeautifulSoup(html_str, 'html.parser')
    assert added_comment in str(soup)
    assert beautiful_soup_utils.LINK_COMMENT not in str(soup)

    print("add css tags so that an internal comment is added")
    beautiful_soup_utils.add_css_head_tags(soup, ["dummytag.css"])
    # make sure the internal comment is now there
    assert beautiful_soup_utils.LINK_COMMENT in str(soup)

    print("call remove_html_comnents to remove ALL comments")
    beautiful_soup_utils.remove_html_comments(soup, False)

    assert added_comment not in str(soup)
    assert beautiful_soup_utils.LINK_COMMENT not in str(soup)


def test_has_text_content():
    """ test has_text_content function """

    soup = BeautifulSoup("", "html.parser")
    p_w_content = soup.new_tag("p")
    p_w_content.append("hello!")
    p_wo_content = soup.new_tag("p")
    test_tags = [[p_w_content, True], [p_wo_content, False]]
    for test in test_tags:
        test_tag = test[0]
        test_expected = test[1]
        has_content = beautiful_soup_utils.has_text_content(test_tag)
        print("Tag: " + str(test_tag))
        print("Has text content? " + str(has_content))
        assert has_content == test_expected
    print("pass")


def test_encapsulate():
    """ test encapsulate_tag_text function """

    tag_text = "Hello"
    p_tag_class = "a"  # css class for <p> tag
    p_tag_open = '<p class="{}">'.format(p_tag_class)
    # original p tag with bare, unwrapped text inside
    original_tag = '{}{}</p>'.format(p_tag_open, tag_text)
    wrap_class = "newtag"  # css class for wrapping <span>
    # p tag with that bare text wrapped in a <span>
    wrapped_tag = '{}<span class="{}">{}</span></p>'.format(
            p_tag_open, wrap_class, tag_text)

    html_str = '''
<html>
    <head></head>
    {}
    <body>
    </body>
</html>'''.format(original_tag)
    print("general basic beautifulsoup with one comment")
    soup = BeautifulSoup(html_str, 'html.parser')
    assert original_tag in str(soup)
    assert wrapped_tag not in str(soup)

    print("call encapsulate_tag_text to encapsulate a <p> tag in a <span>")
    beautiful_soup_utils.encapsulate_tag_text(
            soup,
            "p", {"class": p_tag_class},
            "span", {"class": wrap_class},
            True)
    assert wrapped_tag in str(soup)
    print("pass")


def string_in_file(filepath, string):
    """
    Check if a string (or regex) is in a file

    :param string filepath: path to file
    :param (string or regex) string: string
    or regex to look for
    """
    with open(filepath) as myfile:
        if re.findall(string, myfile.read()):
        # if string in myfile.read():
            return True
    return False


def test_preserve_ru():
    """
    Test write_soup_to_file, while preserving Cyrillic text
    """
    outfile = os.path.join(OUTPUT_DIR, "test_preserve_ru.html")

    # soup to use
    ru = "проверьте русский"
    html_base = '''
        <html>
        <head></head>
        <body>
            <span>{}</span>
            <br>
            <span>Test&nbsp;non-breaking space!</span>
            <br>
            <span>    Test span with space in it   </span>
        </body>
    </html>'''.format(ru)
    soup = BeautifulSoup(html_base, "html.parser")

    print("Write soup to file, preserving Cyrillic, but not &nbsp;")
    beautiful_soup_utils.write_soup_to_file(soup, outfile, True, True, False)
    assert string_in_file(outfile, ru)
    assert not string_in_file(outfile, "&nbsp;")


def test_write_preserve_nbsp():
    """
    Test write_soup_to_file, while preserving &nbsp; chars
    """
    outfile = os.path.join(OUTPUT_DIR, "test_preserve_nbsp.html")

    # soup to use
    ru = "проверьте русский"
    html_base = '''
        <html>
        <head></head>
        <body>
            <span>{}</span>
            <br>
            <span>Test&nbsp;non-breaking space!</span>
            <br>
            <span>    Test span with space in it   </span>
        </body>
    </html>'''.format(ru)
    soup = BeautifulSoup(html_base, "html.parser")

    print("Write soup to file, preserving &nbsp; but not Cyrillic")
    beautiful_soup_utils.write_soup_to_file(soup, outfile, True, False, True)
    assert string_in_file(outfile, "&nbsp;")
    assert not string_in_file(outfile, ru)


def test_write_preserve_both_ru_and_nbsp():
    """
    Test write_soup_to_file, while preserving Cyrillic
    text and &nbsp; chars
    """
    outfile = os.path.join(OUTPUT_DIR, "test_preserve_nbsp.html")

    # soup to use
    ru = "проверьте русский"
    html_base = '''
        <html>
        <head></head>
        <body>
            <span>{}</span>
            <br>
            <span>Test&nbsp;non-breaking space!</span>
            <br>
            <span>    Test span with space in it   </span>
        </body>
    </html>'''.format(ru)
    soup = BeautifulSoup(html_base, "html.parser")

    print("Write soup to file, preserving &nbsp; but not Cyrillic")
    beautiful_soup_utils.write_soup_to_file(soup, outfile, True, True, True)
    assert string_in_file(outfile, "&nbsp;")
    assert string_in_file(outfile, ru)


def test_write_collapse_ws_inner():
    """
    Test write_soup_to_file, while collapsing whitespace
    inside of specified tags
    """
    outfile = os.path.join(OUTPUT_DIR, "test_collapse_ws_inner.html")

    # soup to use
    span_text = "Test span with space in it"
    span = "    {}   ".format(span_text)
    html_base = '''
        <html>
        <head></head>
        <body>
            <span>проверьте русский</span>
            <br>
            <span>{}</span>
        </body>
    </html>'''.format(span)
    soup = BeautifulSoup(html_base, "html.parser")

    print("Write soup to file, collapsing whitespace within <span> tags")
    beautiful_soup_utils.write_soup_to_file(
            soup, outfile, True, True, True, ["span"])
    assert string_in_file(outfile, span_text)
    assert not string_in_file(outfile, span)


def test_write_collapse_ws_outer():
    """
    Test write_soup_to_file, while collapsing whitespace
    outside of specified tags
    """
    outfile = os.path.join(OUTPUT_DIR, "test_collapse_ws_outer.html")

    # soup to use
    html_base = '''
        <html>
        <head></head>
        <body>
            <span>проверьте русский</span>
            <br>
            <span>    Test span with space in it   </span>
        </body>
    </html>'''
    soup = BeautifulSoup(html_base, "html.parser")

    print("Write soup to file, collapsing whitespace surrounding <span> tags")
    beautiful_soup_utils.write_soup_to_file(
            soup, outfile, True, True, True, [], ["span"])

    assert string_in_file(outfile, "<body><span>")
    assert string_in_file(outfile, "<br/><span>")
    assert string_in_file(outfile, "</span><br/>")
    assert string_in_file(outfile, "</span></body>")
    assert not string_in_file(outfile, r'\s+<span>')  # should be no spaces before <span>


def test_write_collapse_ws_both():
    """
    Test write_soup_to_file, while collapsing whitespace
    inside and out of specified tags
    """
    outfile = os.path.join(OUTPUT_DIR, "test_collapse_ws_inner_outer.html")

    # soup to use
    span_text = "Test span with space in it"
    span = "    {}   ".format(span_text)
    html_base = '''
        <html>
        <head></head>
        <body>
            <span>проверьте русский</span>
            <br>
            <span>{}</span>
        </body>
    </html>'''.format(span)
    soup = BeautifulSoup(html_base, "html.parser")

    print("Write soup to file, collapsing whitespace within " +
          "<span> tags and outside")
    beautiful_soup_utils.write_soup_to_file(
            soup, outfile, True, True, True, ["span"], ["span"])
    assert string_in_file(outfile, span_text)
    assert not string_in_file(outfile, span)
    assert string_in_file(outfile, "<body><span>")
    assert string_in_file(outfile, "<br/><span>")
    assert string_in_file(outfile, "</span><br/>")
    assert string_in_file(outfile, "</span></body>")
    assert not string_in_file(outfile, r'\s+<span>')  # should be no spaces before <span>


def main(args):
    # Get all functions in current file
    functions_list = inspect.getmembers(
            sys.modules['__main__'], inspect.isfunction)
    # run the functions that begin with test_
    for name, func in functions_list:
        if name.startswith("test_"):
            func()


if __name__ == "__main__":
    main(sys.argv[1:])
