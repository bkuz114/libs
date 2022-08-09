import os
import sys
import distutils.dir_util
import shutil

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

'''
Takes abs path to <src> dir and <dest> dir, and
cp -r <src> into <dest>
overwrites <dest>/<src> if exists

Example:
if you have folder /a/b/c/
and you want to copy 'c' and contents to
path /a/d/e/f/,
  copy_folder_recursively('a/b/c/', 'a/d/e/f/')
results in:
    /a/d/e/f/c/
'''
def copy_folder_recursively(src, dest):
    if not os.path.isabs(src) or not os.path.isabs(dest):
        sys.exit("ERROR: (io_utils): can't copy folder - either src or dest is not absolute!")

    src_dir = src
    # need to get top level folder name to construct dest path
    # (i.e. if 'a/b/c' want 'c')
    # os.path.basename will return empty string if path ends in '/' char
    # so strip it off if its there
    if src_dir.endswith("/"):
        src_dir = ASSETS_DIR[:-1] # strips off last char of string

    src_foldername = os.path.basename(src_dir)
    dest_dir = os.path.abspath(os.path.join(dest, src_foldername))

    # check if src and dest are same (distutils will fail if they are)
    if not src_dir == dest_dir:
        # shutil will fail if the dest dir exists
        # update : FYI dirs_exist_ok corrects problem of existing dir, but using distutils now so just going to keep using
        #shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
        # https://stackoverflow.com/questions/10047521/how-to-copy-directory-with-all-file-from-c-xxx-yyy-to-c-zzz-in-python/17358075
        distutils.dir_util.copy_tree(src_dir, dest_dir)
        # distutils depracated? go back to shutil eventually?
