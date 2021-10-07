import os

ENC = 'utf-8'

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


