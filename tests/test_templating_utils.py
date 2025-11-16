import sys
import os
sys.path.append("..")
import templating_utils

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

to_template = '''
First, I want to template {these strings} that {are in} curly brackets.
Second, I want to template [these] and [these that are] in hard brackets.
'''
print("ORIGINAL TEXT:")
print(to_template)

print("\n ==== Test #1: Template {, } delims (no &nbsp; padding) ==== ")
templated = templating_utils.template_string(
        to_template, "{", "}", "span",
        {"class": "a b c"}, False)
print(templated)

print("\n ==== Test #2: Template [, ] delims (no &nbsp; padding) ==== ")
templated = templating_utils.template_string(
        to_template, "[", "]", "span",
        {"class": "a b c"}, False)
print(templated)

print("\n ==== Test #3: Template {, } delims (&nbsp; padding) ==== ")
templated = templating_utils.template_string(
        to_template, "{", "}", "span",
        {"class": "a b c"}, True)
print(templated)

print("\n ==== Test #4: Template {, } and [, ] delims (&nbsp; padding) ==== ")
templated = templating_utils.template_string(
        to_template, "{", "}", "span",
        {"class": "a b c"}, True)
templated = templating_utils.template_string(
        templated, "[", "]", "span",
        {"class": "a b c"}, True)
print(templated)



