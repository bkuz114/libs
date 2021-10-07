import os
import sys
from bs4 import BeautifulSoup
import distutils.dir_util
import re

ENC = 'utf-8'

'''
Copies a folder and all contents
into another folder, overwriting existing
(src and dest paths must be absolute)

Example:
if you have folder /a/b/c/
and you want to copy 'c' and contents to
path /a/d/e/f/,
  copy_folder_recursively('a/b/c/', 'a/d/e/f/')
results in:
    /a/d/e/f/c/
'''
def copy_folder_recursively(src, dest):
    print(("\t\tbookutils: cp folder {} --> {}").format(src, dest))
    if not os.path.isabs(src) or not os.path.isabs(dest):
        sys.exit("ERROR: bookutils: can't copy folder - either src or dest is not absolute!")

    src_dir = src
    print("src dir: " + src_dir)
    # need to get top level folder name to construct dest path
    # (i.e. if 'a/b/c' want 'c')
    # os.path.basename will return empty string if path ends in '/' char
    # so strip it off if its there
    if src_dir.endswith("/"):
        src_dir = ASSETS_DIR[:-1] # strips off last char of string
    print("src dir: " + src_dir)
    src_foldername = os.path.basename(src_dir)
    dest_dir = os.path.abspath(os.path.join(dest, src_foldername))
    print("dest dir: " + dest_dir)
    print(("Copy {} to {}").format(src_dir, dest_dir))
    # shutil will fail if the dest dir exists
    #shutil.copytree(src_dir, dest_dir)
    # https://stackoverflow.com/questions/10047521/how-to-copy-directory-with-all-file-from-c-xxx-yyy-to-c-zzz-in-python/17358075
    distutils.dir_util.copy_tree(src_dir, dest_dir)

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
                    chapnum = str(i + 1)
                if not os.path.isabs(filepath):
                    filedir = os.path.dirname(bookinput_filepath)
                    filepath = os.path.abspath(os.path.join(filedir, filepath))
                chapter_data.append([chapnum, chapname, filepath])

    return title, chapter_data

'''
Get contents of a text file as a string
and return the string
'''
def get_file_as_str(filepath):
    print(("\t\tbookutils: Read file: {}").format(filepath))
    if not os.path.isabs(filepath):
        sys.exit(("ERROR: bookutils: can't read {}, path is not absolute!").format(filepath))
    html_file = open(filepath, "r", encoding=ENC)
    html_as_str = html_file.read()
    html_file.close()
    return html_as_str

'''
return a BeautifulSoup object
given a strong of html data
'''
def make_soup(html_str):
    soup = BeautifulSoup(html_str.encode(ENC), 'html.parser')
    return soup

'''
take a BeautifulSoup object an an abs path
and writes to an html file
at the specified path
fails if not an abs path.
'''
def write_soup_to_file(soup, output_filename, force):
    # write to html
    print(("\tbookutils: Prettify soup...").format(output_filename))
    soup.prettify(formatter='html')

    if not os.path.isabs(output_filename):
        sys.exit("ERROR: 'write_soup_to_file' - output_filename is not absolute!")

    if os.path.exists(output_filename) and not force:
        sys.exit(('''\n
ERROR! An output file, {}, already exists!
Solutions:\n
\t1. Specify different output dir using --output\n
\t2. Give --timestamp flag\n
\t3. Give --FORCE option (will overwrite existing files, be careful''').format(output_filename))

    # create dirs in path if they don't exist
    basedir = os.path.dirname(output_filename)
    if not os.path.exists(basedir):
        print(("\t\tbookutils: Make dirs in path : {}").format(basedir))
        os.makedirs(basedir)

    if force:
        print(("\tbookutils: Write file {} ('force' given; overwrite existing)...").format(output_filename))
        wr = open(output_filename, "w", encoding=ENC)
    else:
        print(("\tbookutil: Write file {} ...").format(output_filename))
        wr = open(output_filename, "x", encoding=ENC)
    wr.write(str(soup))
    wr.close()
    return output_filename
