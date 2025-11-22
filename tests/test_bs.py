import inspect
import sys
import os
import datetime
sys.path.append("..")
import beautiful_soup_utils
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

soup = BeautifulSoup("", 'html.parser')

filepath = os.path.join(SCRIPT_DIR, "basic.html")
# create a timestamped output dir
output_dir_base = os.path.join(SCRIPT_DIR, "output_test_bs")
fmt = "%Y_%m_%d-%H_%M_%S"
ct = datetime.datetime.now().strftime(fmt)
output_dir = os.path.abspath(os.path.join(output_dir_base, ct))
bs = beautiful_soup_utils.make_soup_from_file(filepath)
new_h1 = soup.new_tag("h1")
print(bs)


def test_add_classes():
    print("--- test add_classes function ---")
    h1 = soup.new_tag("h1")
    print("initial h1 tag:")
    print(h1)
    print("add css classes to this tag")
    beautiful_soup_utils.add_classes(h1,["hello", "me"])
    beautiful_soup_utils.add_classes(h1,["more", "stuff"])
    beautiful_soup_utils.add_classes(h1,["more", "stuff"])
    print("after adding classes:")
    print(h1)

def test_find_replace():
    print("---- new try find replace ---")
    print("soup before:")
    print(bs)
    beautiful_soup_utils.find_replace_str(bs, "Hello", "Goodbye :(")
    beautiful_soup_utils.find_replace_str(bs, "World", "Sweet, Sweet World")
    print("after:")
    print(bs)
    print("now add a beautiful soup tag to it.")
    beautiful_soup_utils.find_replace_str(bs, "Goodbye", new_h1)
    print(bs)

def test_css_classes():
    print("---- add/remove/get css classes from tag ---")
    print("create an h1 tag...")
    h1 = soup.new_tag("h1")
    print("tag initial:")
    print(h1)
    print("Get css classes from tag:")
    classes = beautiful_soup_utils.get_classes(h1)
    print("Class list returned:")
    print(classes)
    classes_to_add = ["mmmm", "here2", "here5"]
    print("add classes: " + str(classes_to_add))
    beautiful_soup_utils.add_classes(h1, classes_to_add)
    print("soup after")
    print(h1)
    classes_to_remove = ["mmmm", "here2", "h343", "here1"]
    print("Remove classes: " + str(classes_to_remove))
    beautiful_soup_utils.remove_classes(h1, classes_to_remove)
    print("soup after")
    print(h1)

def test_head_tags():
    # test out adding head tags
    print("----- add css head tags ----")
    paths = ["dummy1", "dummy2"]
    print("add css head tags: " + str(paths) + " (appends to END of <head> by default)")
    beautiful_soup_utils.add_css_head_tags(bs, paths)
    paths2 = ["dummy-ind1", "./assets/dummy-ind2"]
    print("add css head tags: " + str(paths2) + " at index 0")
    beautiful_soup_utils.add_css_head_tags(bs, paths2, startAt=0)
    paths3 = ["dummy-ind-mid1", "/here/dummy-ind-mid2"]
    print("add css head tags: " + str(paths3) + " at index 3")
    beautiful_soup_utils.add_css_head_tags(bs, paths3, startAt=3)

def test_print_tags():
    # make some random tags and print them..
    print("---- Make some head tags for fun (these are NOT included anywhere in final file) ----")
    js_tags = ["./assets/tag1.js", "./assets/js/tag2.js"]
    css_tags = ["./assets/css/tag1.css", "./assets/css/tag2.css"]
    for tag in js_tags:
        print("Make a js tag for path: " + tag)
        print("\t{}".format(str(beautiful_soup_utils.js_tag(tag))))
    for tag in css_tags:
        print("Make a css tag for path: " + tag)
        print("\t{}".format(str(beautiful_soup_utils.css_tag(tag))))

def test_update_tag_paths():
    # update paths in head tags
    rel = "../.."
    print("\n --- Update the head tags to be relative to " + rel)
    print("soup before:")
    print(bs.prettify())
    beautiful_soup_utils.update_paths(bs, rel)
    print("soup after:")
    print(bs.prettify())

def test_remove_comments():
    # remove HTML comments, except for the internal
    # ones added
    print("\n -- Remove HTML comments except internal ones added by library")
    print("soup before:")
    print(bs.prettify())
    beautiful_soup_utils.remove_html_comments(bs, True)
    print("soup after:")
    print(bs.prettify())

    # remove ALL comments
    print("\n -- Remove ALL comments remaining")
    print("soup before:")
    print(bs.prettify())
    beautiful_soup_utils.remove_html_comments(bs, False)
    print("soup after:")
    print(bs.prettify())

def test_has_content():
    # test has_text_content method
    print(" --- text 'has_text_content' function ---")
    p_w_content = soup.new_tag("p")
    p_w_content.append("hello!")
    p_wo_content = soup.new_tag("p")
    test_tags = [p_w_content, p_wo_content]
    for test_tag in test_tags:
        print("Next tag: " + str(test_tag))
        print("Has content? " + str(beautiful_soup_utils.has_text_content(test_tag)))

def test_encapsulate():
    # search <p> tags and put text in it in <span> tags
    print("\n --- test encapsulate_tag_text ---")
    print("soup before:")
    print(bs.prettify())
    beautiful_soup_utils.encapsulate_tag_text(
            bs, "p", {"class": "a"}, "span", {"class": "newtag"}, True)
    print("soup after:")
    print(bs.prettify())
    return True

def test_write_soup():
    # writing soup to file
    print("\n -- Test writing soup to file in different configurations")
    outfile1 = os.path.join(output_dir, "save-ru.html")
    outfile2 = os.path.join(output_dir, "save-nbsp.html")
    outfile3 = os.path.join(output_dir, "save-ru-save-nbsp.html")
    outfile4 = os.path.join(output_dir, "save-collapse-inner.html")
    outfile5 = os.path.join(output_dir, "save-collapse-outer.html")
    outfile6 = os.path.join(output_dir, "save-collapse-both.html")
    print("\n    1. write soup to file, preserving Cyrillic, but not &nbsp;")
    beautiful_soup_utils.write_soup_to_file(bs, outfile1, True, True, False)
    print("\n    2. write soup to file, preserving &nbsp; but not Cyrillic")
    beautiful_soup_utils.write_soup_to_file(bs, outfile2, True, False, True)
    print("\n    3. write soup to file, preserving Cyrillic and &nbsp;")
    beautiful_soup_utils.write_soup_to_file(bs, outfile3, True, True, True)
    print("\n    4. write soup to file, collapsing whitespace within <span> tags")
    beautiful_soup_utils.write_soup_to_file(bs, outfile4, True, True, True, ["span"])
    print("\n    5. write soup to file, collapsing whitespace surrounding <span> tags")
    beautiful_soup_utils.write_soup_to_file(bs, outfile5, True, True, True, [], ["span"])
    print("\n    6. write soup to file, collapsing whitespace inside and out of <span> tags")
    beautiful_soup_utils.write_soup_to_file(bs, outfile6, True, True, True, ["span"], ["span"])


def main(args):
    # Get all functions in current file
    functions_list = inspect.getmembers(sys.modules['__main__'], inspect.isfunction)
    # run the functions that begin with test_
    for name, func in functions_list:
        if name.startswith("test_"):
            func()

if __name__ == "__main__":
    main(sys.argv[1:])
