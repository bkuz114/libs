import os
import copy
import re
import io_utils
from bs4 import BeautifulSoup

ENC = 'utf-8-sig'

'''
adds a list of css classes to a BeautifulSoup tag.
will not add classes which are already present.
This helper method is useful because a tag's 'class'
attr can be either a String or a list.
Handles adding in either scenario.

Arguments:
----------
    tag
        A BeautifulSoup object
    class_list
        list. List of Strings which are css classes to add
Returns:
--------
    None. Permenantly modifies tag
'''
def add_classes(tag, class_list):
    if 'class' in tag.attrs:
        '''
        BeautifulSoup tag's 'class' attr
        could be either String or list
        '''
        curr_classes = tag['class']
        if type(curr_classes) == type("string"):
            # dont add dupes
            for new_class in class_list:
                if new_class not in curr_classes:
                    tag['class'] += " " + new_class
            #tag['class'] = tag['class'] + " " + " ".join(class_list)
        elif type(curr_classes) == type([]):
            # don't add dupes
            final_list = curr_classes
            final_list.extend(x for x in class_list if x not in final_list)
            tag['class'] = final_list
            #tag['class'].extend(final_list)
        else:
            raise Exception("Can't identify type of tag's 'class' attr")
    else:
        tag['class'] = class_list

'''
Replaces *first* occurance of a String in a BeautifulSoup object
with some other content.
Content can be either another String, or another BeautifulSoup object

Use case example:
----------------
    * html doc with template vars %TITLE% or %MAIN-CONTENT%
    * you generate that info somewhere else, then call this method to swap it in
    beautiful_soup_utils.find_replace_str(my_soup, "%TITLE%, "my great title")
    beautiful_soup_utils.find_replace_str(my_soup, "%MAIN-CONTENT%", my_soup_div)

Arguments:
----------
    soup:
        BeautifulSoup object to search through
    string:
        String. String to replace
    content:
        String or BeautifulSoup object.
        What you will replace String with.
        (can be <class 'bs4.BeautifulSoup.tag'> or even
        <class 'bs4.BeautifulSoup'>)
    allow_empty:
        Boolean. Optional, defaults to False.
        If True, don't raise exception if string not found in soup

Returns:
--------
    None; modifies the soup permenantly.

Warnings:
--------
    ** If content is BeauitulfSoup object,
    will convert it to String, then back to BeautifulSoup object,
    before adding in to soup as replacement for string.
    This could change the type of attributes you're expecting;
    i.e. if you had set a boolean attribute in content,
    it will be type String when it's done.
'''
def find_replace_str(soup, string, content, allow_empty=False):
    found = soup.find(string=re.compile(string))
    '''
    soup.find with string arg will return a NavigableString
    for the ENTIRE string of the tag that contains the string
    (i.e. suppose you have <h1>%TITLE% %NUMBER%</h1>
    soup.find(string=re.compile("%TITLE%"))
       --> returns "%TITLE% %NUMBER%")
    - if you were to directly replace_with on the find result,
    you'll be replacing the entire text of the tag, not just
    the part of the string that matches. Hence the loginc below:

    1. cast returned NavigableString to string
    2. cast content to replace with to string
    3. use standard string replace on 1.,
       to replace ONLY desired match text
       with 2.
    4. convert result of 3. to BeautifulSoup
    5. Finally, do the replace_with with 4.
    '''
    if found:
        found_string = str(copy.copy(found))
        found_replaced = found_string.replace(string, str(content))
        found_replaced = BeautifulSoup(found_replaced, 'html.parser') 
        found.replace_with(found_replaced)
    elif not allow_empty:
        raise Exception("Can't find string {} in soup!".format(string))

'''
doesn't work yet
'''
def replace_all_occurances_in_doc(soup, find, replace_with):
    matches = soup.find_all(text=re.compile(find))
    for mmatch in matches:
        mmatch.replace_with(replace_with)

'''
add script tags to head of document
from list of paths

soup: BeautifulSoup4 object
paths: list of Strings, which should be src urls to the script
    if rel paths, make sure they are rel the HTML doc you're adding to,
    for where its final location will be.

** Note - this will append them to END of <head>; the order is important.
   example - if you are adding a script which uses jquery, you'd need jquery
   script tag to come before the script which relies on it.
'''
def add_js_head_tags(soup, paths):
    for path in paths:
        soup.head.append(BeautifulSoup('<script src="' + path + '"></script>', "html.parser"))

'''
add <link> tags to <head> of document
from list of paths (would use this to add
css files)

soup: BeautifulSoup4 object
paths: list of Strings, which should be paths to the css files
  if giving rel paths, make sure they are rel the HTML doc you'd
  be adding this to (where its final location will be)
'''
def add_css_head_tags(soup, paths):
    for path in paths:
        soup.head.append(BeautifulSoup('<link rel="stylesheet" href="' + path + '" type="text/css">', "html.parser"))

'''
Takes a String of (hopefully) valid HTML
and returns a BeautifulSoup object for
the String.
'''
def make_soup(html_str):
    soup = BeautifulSoup(html_str.encode(ENC), 'html.parser')
    return soup


'''
takes filepath to file,
and returns a BeautifulSoup object
for text in file

Arguments:
----------
    filepath.
        String. Absolute path to filename
        to read.

Returns:
--------
    BeautifulSoup object from data read
    in the input file.
'''
def make_soup_from_file(filepath):
    print(("\t\tbeautiful_soup_utils: Generate soup from file\n\t\t\t{}").format(filepath))
    if not os.path.abspath(filepath):
        raise Exception(
            ("ERROR (beautiful_soup_utils) filepath to get soup from is not absolute {}").format(filepath))
    if not os.path.exists(filepath):
        raise Exception(
            ("ERROR (beautiful_soup_utils) filepath to get soup from does not exist {}").format(filepath))
    file_str = io_utils.get_file_as_str(filepath)
    soup = make_soup(file_str)
    return soup


'''
Takes a BeautifulSoup object,
prettifies it and writes to
an output file.

Arguments:
----------
    soup:
        BeautifulSoup object to write
        to file
    output_filename:
        String. Absolute path to file
        to write to.
    force:
        Boolean. Required. Overwrite
        if files exists
'''
def write_soup_to_file(soup, output_filename, force):
    print(("\t\tbeautiful_soup_utils: Prettify soup and write to\n\t\t\t{}").format(output_filename))
    pretty_soup = soup.prettify(formatter='html')
    io_utils.write_str_to_file(pretty_soup, output_filename, force)
