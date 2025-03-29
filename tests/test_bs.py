import sys
import os
sys.path.append("..")
import beautiful_soup_utils
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

soup = BeautifulSoup("", 'html.parser')

filepath = os.path.join(SCRIPT_DIR, "basic.html")
filepath_out = os.path.join(SCRIPT_DIR, "basic_modified.html")
bs = beautiful_soup_utils.make_soup_from_file(filepath)
print(bs)

h1 = bs.find("h1")
print(h1)
beautiful_soup_utils.add_classes(h1,["hello", "me"])
print(h1)
beautiful_soup_utils.add_classes(h1,["more", "stuff"])
print(h1)
beautiful_soup_utils.add_classes(h1,["more", "stuff"])
print(h1)
print("get as string")
bs_str = str(bs)
bs_back = BeautifulSoup(bs_str, 'html.parser')
print("converted back bs")
print(bs_back)
h1_now = bs_back.find("h1")
print("found h1")
print(h1_now)
beautiful_soup_utils.add_classes(h1_now, ["addmore"])
print(h1_now)
new_h1 = soup.new_tag("h1")
new_h1['class'] = "myclass"
print("my new h1")
print(new_h1)
beautiful_soup_utils.add_classes(new_h1, ["here1", "here2"])
print(new_h1)
beautiful_soup_utils.add_classes(new_h1, ["here1", "here2"])
print(new_h1)

print("---- new try find replace ---")
print("soup before:")
print(bs)
beautiful_soup_utils.find_replace_str(bs, "Hello", "Goodbye :(")
print(bs)
beautiful_soup_utils.find_replace_str(bs, "World", "Sweet, Sweet World")
print(bs)
print("now add a beautiful soup tag to it.")
beautiful_soup_utils.find_replace_str(bs, "Goodbye", new_h1)
print(bs)
print(new_h1)

print("---- add/remove/get css classes from tag ---")
print("h1 before:")
print(new_h1)
print("Get class list:")
classes = beautiful_soup_utils.get_classes(new_h1)
print("Class list returned:")
print(classes)
classes_to_add = ["mmmm"]
print("add classes: " + str(classes_to_add))
beautiful_soup_utils.add_classes(new_h1, classes_to_add)
print("soup after")
print(new_h1)
classes_to_remove = ["mmmm", "here2", "h343", "here1"]
print("Remove classes: " + str(classes_to_remove))
beautiful_soup_utils.remove_classes(new_h1, classes_to_remove)
print("soup after")
print(new_h1)

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

# update paths in head tags
rel = "../.."
print("\n --- Update the head tags to be relative to " + rel)
print("soup before:")
print(bs.prettify())
beautiful_soup_utils.update_paths(bs, rel)
print("soup after:")
print(bs.prettify())

# test has_text_content method
print(" --- text 'has_text_content' function ---")
p_w_content = soup.new_tag("p")
p_w_content.append("hello!")
p_wo_content = soup.new_tag("p")
test_tags = [p_w_content, p_wo_content]
for test_tag in test_tags:
    print("Next tag: " + str(test_tag))
    print("Has content? " + str(beautiful_soup_utils.has_text_content(test_tag)))

# write this to file
print("---- Tests over... write it to file... ---")
beautiful_soup_utils.write_soup_to_file(bs, filepath_out, True) 
