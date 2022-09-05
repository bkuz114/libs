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
print("add data to h1")
beautiful_soup_utils.add_classes(new_h1, ["mmmm"])
print("soup after")
print(bs)
print(new_h1)

# test out adding head tags
paths = ["dummy1", "dummy2"]
beautiful_soup_utils.add_css_head_tags(bs, paths)
paths2 = ["dummy-ind1", "dummy-ind2"]
beautiful_soup_utils.add_css_head_tags(bs, paths2, startAt=0)
paths3 = ["dummy-ind-mid1", "dummy-ind-mid2"]
beautiful_soup_utils.add_css_head_tags(bs, paths3, startAt=3)

# write this to file
beautiful_soup_utils.write_soup_to_file(bs, filepath_out, True) 
