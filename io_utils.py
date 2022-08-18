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
copies file at src to dest
- if dest is an EXISTING dir, rather than a filepath,
  creates file with identical basename as src in dest
- makes any dirs in path to dest if they don't exist.
- if you've give dest as a dirpath
  (path has no file extension, like i.e. a/b/c/d)
  but path doesn't yet exist, will assume you want to
  copy to file called d - it will NOT take this as a dir
  In such a case, create the dir you want before
  calling this function, i.e.
    os.makedirs(dest)
    copy_file(src, dest)
  would do this for you, but what if you really want to
  copy to a file that's just bare with no extension?

ex: copy_file("a/b/c.txt", "a/b/d.txt")
copies the files a/b/c.txt --> a/b/d.txt
'''
def copy_file(src, dest, force=False):
    if not os.path.isabs(src) or not os.path.isabs(dest):
        raise Exception("ERROR io_utils:copy_file: src or dest are not absolute")
    if not os.path.exists(src):
        raise Exception("ERROR io_utils:copy_file: src to copy doesn't exist! src: {}".format(src))
    # fail if dest exists and isn't a dir
    if not force and os.path.exists(dest) and not os.path.isdir(dest):
        raise Exception("ERROR io_utils:copy_file: dest to copy to, {}, already exists (to copy anyway, rerun with force=True))".format(dest))
    os.makedirs(os.path.dirname(dest), exist_ok=True) # exist_ok doesn't alter anything; just prevents err from being raised if dest exists
    '''
    if you ever change from using shutil.copy,
    make sure new method does what you claim in this function,
    ex., if dest is a dir, shutil.copy creates a file with basename
    of src and puts that in dest; if dest a filename just copies
    it directly there.
    https://docs.python.org/2.7/library/shutil.html?highlight=shutil.copy#shutil.copy
    '''
    shutil.copy(src, dest)

'''
copies list of filepaths to a dest folder.
(For each file in files, creates a file wit
identical basename in dest)
optional arg force allows copy to continue
if any of the resulting dest files exists.

- dest and all src files should be abs paths
(if src file isn't abs, will only fail once copy_file
is called)
'''
def copy_files(files, dest, force=False):
    if not os.path.isabs(dest):
        raise Exception("ERROR io_utils:copy_files: dest dir is not absolute! {}".format(dest))
    if os.path.exists(dest) and not os.path.isdir(dest):
        raise Exception("ERROR io_utils:copy_files: dest exists is not a dir! {}".format(dest))
    os.makedirs(dest, exist_ok=True)
    for file in files:
        copy_file(file, dest, force)

'''
Takes abs path to <src> dir and <dest> dir, and
cp -r <src> <dest>
overwrites <dest>/<src> if exists

Optional arg explode will explode the dir
in to dest, i.e.
cp -r <src>/. <dest>

Example:
if you have folder /a/b/c/
and you want to copy 'c' and contents to
path /a/d/e/f/,
  copy_folder_recursively('a/b/c/', 'a/d/e/f/')
results in:
    /a/d/e/f/c/
  copy_folder_recursively('a/b/c/', a/d/e/f/', explode=True)
results in
    all contents of '/a/b/c/' copied directly in to a/d/e/f/
'''
def copy_folder_recursively(src, dest, explode=False):
    if not os.path.isabs(src) or not os.path.isabs(dest):
        sys.exit("ERROR: (io_utils): can't copy folder - either src or dest is not absolute!")

    src_dir = src
    # need to get top level folder name to construct dest path
    # (i.e. if 'a/b/c' want 'c')
    # os.path.basename will return empty string if path ends in '/' char
    # so strip it off if its there
    if src_dir.endswith("/"):
        src_dir = src_dir[:-1] # strips off last char of string

    src_foldername = os.path.basename(src_dir)
    dest_dir = dest
    if not explode:
        dest_dir = os.path.join(dest, src_foldername)
    dest_dir = os.path.abspath(dest_dir)

    # check if src and dest are same (distutils will fail if they are)
    if not src_dir == dest_dir:
        # shutil will fail if the dest dir exists
        # update : FYI dirs_exist_ok corrects problem of existing dir, but using distutils now so just going to keep using
        #shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
        # https://stackoverflow.com/questions/10047521/how-to-copy-directory-with-all-file-from-c-xxx-yyy-to-c-zzz-in-python/17358075
        distutils.dir_util.copy_tree(src_dir, dest_dir)
        # distutils depracated? go back to shutil eventually?

'''
Return list of paths to all immediate files in a directory.
Optional boolean arg names only returns names of the files (not full paths)

Arguments:
----------

folder:
    name of folder to list files in.
    Does not need to be abspath.
    if rel. path, should be be rel dir
    where script that imported this script
    is being called.
    e.g.: script a.py in dir /a/b/c/ imports io_utils and calls
    list_subdirs; you call a.py from /a/b/;
    the rel path to 'folder' should be rel /a/b/

names:
    optional boolean. If True, only return names of the
    files. If False, returns abs. paths to the files.

throws exception if folder does not exist

https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
 (answer by gahooa)
'''
def list_files(folder, names=False):
    files = []
    if names:
        files = [ f.name for f in os.scandir(folder) if f.is_file() ]
    else:
        files = [ f.path for f in os.scandir(folder) if f.is_file() ]
    return files

'''
Return list of paths to all immediate subdirs in a directory.
Optional boolean arg names only returns names of the dirs (not full paths)

Arguments:
----------

folder:
    name of folder to get subdirs of.
    Does not need to be abspath.
    if rel. path, should be be rel dir
    where script that imported this script
    is being called.
    e.g.: script a.py in dir /a/b/c/ imports io_utils and calls
    list_subdirs; you call a.py from /a/b/;
    the rel path to 'folder' should be rel /a/b/

names:
    optional boolean. If True, only return names of the
    dirs. If False, returns abs. paths to the dirs.

throws exception if folder does not exist

https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
 (answer by gahooa)
'''
def list_subdirs(folder, names=False):
    subfolders = []
    if names:
        subfolders = [ f.name for f in os.scandir(folder) if f.is_dir() ]
    else:
        subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    return subfolders
