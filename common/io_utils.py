import os
import sys

ENC = 'utf-8'

'''
filepath: absolute path to a file.
Reads text content and returns as String
'''
def get_file_as_str(filepath):
    if not os.path.isabs(filepath):
        sys.exit(("ERROR: (io_utils): can't read {}, path is not absolute!").format(filepath))
    if not os.path.exists(filepath):
        sys.exit(("ERROR: (io_utils): Can't read {}; file does not exist!").format(filepath))

    file = open(filepath, "r", encoding=ENC)
    file_str = file.read()
    file.close()
    return file_str

'''
filepath: absolute path to a file.
Writes string to file at specified path.
Makes dirs in path if they do not exist.
force arg allows overwrite if file exists
'''
def write_str_to_file(string, filepath, force):
    if not os.path.isabs(filepath):
        sys.exit(("ERROR: (io_utils.py) Output file not absolute! (Output file: {})").format(filepath))

    if os.path.exists(filepath) and not force:
        sys.exit(("ERROR: (io_utils.py) Output file {} exists (your script should call this function with force arg as True)").format(filepath))
    # create dirs in path if they don't exist
    basedir = os.path.dirname(filepath)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    if force:
        wr = open(filepath, "w", encoding=ENC)
    else:
        wr = open(filepath, "x", encoding=ENC)
    wr.write(string)
    wr.close()
