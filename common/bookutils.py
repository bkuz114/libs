import os
import sys
from bs4 import BeautifulSoup
import re
import datetime

# other py files in this common lib
import io_utils

ENC = 'utf-8'

# a generic BeautifulSoup object to use throughtout script
# for basic functions
SOUP = BeautifulSoup("", 'html.parser')

'''
Generate a timestamp string with no spaces
'''
def timestamp():
    # format the datetime without any spaces
    fmt = "%Y_%m_%d-%H_%M_%S"
    ct = datetime.datetime.now().strftime(fmt)
    return str(ct)

'''
Takes an abs path to a data file for a book,
Parses data file, and returns:
<book title>, <chapter_data>
where <chapter_data> is an array of arrays;
one array for each chapter of format [<chapter name>, <filepath>]
i.e.:
[["chapter1", "filepath"],["chapter2", "filepath2"],...]
filepaths can be rel or absolute.
if rel, will resolve based on data files directory.

Data file that is parsed should be of format:
Line 1: <book title>
Line 2: <chapter #>:<chapter name>:<filepath to chapter>
Line 3: ..
so on.

If you do NOT want to fill out chapter # that is OK.
You can omit them, but still keep the ':'. ex:
:myChap:/my/path.txt

In this case, the chapter numbers will be generated based on
line numbers.

'''
def parse_data_file(bookinput_filepath):

    title = ""
    chapter_data = []
    
    print(("\nParse book data file {} to get chapter list...").format(bookinput_filepath))

    if not os.path.isabs(bookinput_filepath):
        sys.exit("Error! (from bookutils.py common lib): Path to book input is not absolute!")

    # get input file which has title and list of chapters and locations
    with open(bookinput_filepath, 'r', encoding=ENC) as f: # readonly mode
        lines = f.readlines()

        found_title = False
        chap_num_counter = 1
        for i, line in enumerate(lines):   
            line = line.strip() # make sure this is before check for empty line!
            if not line or line.startswith("#"):
                continue

            if not found_title:
                # title
                title = line
                found_title = True
            else:
                # line will be chapter title : filepath
                parse_line = line.split(":")
                if len(parse_line) < 3:
                    sys.exit(('''\n
ERROR: Line {} of input ile {} -\n
Can't parse line. Expecting format <chap #>:<chap title>:<filepath>,
but not enough ':' chars were found.\n
(You can omit chapter numbers, and the script will generate them based on the order of the lines. But you will need two ':' on each line, just keep blank space before first ':'\n
i.e. :myChap:/filepath/file.txt)''').format(i, bookinput_filepath))
                # resolve filepath in case it's a relative path
                chapnum = parse_line[0]
                chapname = parse_line[1]
                filepath = parse_line[2]
                if not chapnum:
                    chapnum = str(chap_num_counter)
                if not os.path.isabs(filepath):
                    filedir = os.path.dirname(bookinput_filepath)
                    filepath = os.path.abspath(os.path.join(filedir, filepath))
                chapter_data.append([chapnum, chapname, filepath])
                chap_num_counter += 1

    return title, chapter_data

'''
return a BeautifulSoup object
given a strong of html data
'''
def make_soup(html_str):
    soup = BeautifulSoup(html_str.encode(ENC), 'html.parser')
    return soup

'''
Prettifies BeautifulSoup html and writes
to output file.
output_filename should be abs path
'''
def write_soup_to_file(soup, output_filename, force):
    print(("\t\tbookutils: Prettify soup and write to {}...").format(output_filename))
    pretty_soup = soup.prettify(formatter='html')
    io_utils.write_str_to_file(pretty_soup, output_filename, force)

'''
takes filepath to file,
and returns a BeautifulSoup object
for text in file
'''
def make_soup_from_file(filepath):
    if not os.path.abspath(filepath):
        sys.exit(("ERROR (bookutils) filepath to get soup from is not absolute {}").format(filepath))
    if not os.path.exists(filepath):
        sys.exit(("ERROR (bookutils) filepath to get soup from does not exist {}").format(filepath))
    file_str = io_utils.get_file_as_str(filepath)
    soup = make_soup(file_str)
    return soup

'''
takes ABS PATH to a text file.
Extracts data and converts in to BeautifulSoup
HTML with <p> tags for each chapter.
'''
def get_chapter_as_div(filepath):
    print(("\t\tbookutils: Parse chapter file {}").format(filepath))

    if not os.path.isabs(filepath):
        sys.exit(("ERROR: filepath to chapter file ({}) is not absolute!").format(filepath))

    chapter_div = SOUP.new_tag("div")
    if os.path.exists(filepath):

        with open(filepath, 'r', encoding=ENC) as f: # readonly mode
            lines = f.readlines()
            # go through and create <p> tags at each newline
            para_tag = SOUP.new_tag("p")
            for i, line in enumerate(lines):
                line = line.strip()
                para_tag.append(line)
                if not line or i == len(lines) - 1:
                    # got to end of paragraph.
                    chapter_div.append(para_tag)
                    para_tag = SOUP.new_tag("p")
    else:
        sys.exit(("Error! Chapter file {} does not exist!").format(filepath))

    return chapter_div
