import sys
import os
from bs4 import BeautifulSoup
import io_utils

ENC = 'utf-8-sig'

'''
Takes a String of (hopefully) valid HTML
and returns a BeautifulSoup object for
the String.
'''
def make_soup(html_str):
    soup = BeautifulSoup(html_str.encode(ENC), 'html.parser')
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
