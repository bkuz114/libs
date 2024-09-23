import os
import sys
import shutil

ENC = 'utf-8'


'''
helper function to
get a file extension,
since I'm always forgetting
hot to call it...

file_ext("a.txt")
    returns "txt"
file_ext("b")
    returns ""
'''


def file_ext(path):
    file_ext = os.path.splitext(path)[1]
    # if there's an extension,
    # returns it WITH the .
    # i.e. file_ext = ".txt"
    # want to remove the .
    if file_ext:
        return file_ext[1:]
    return ""


'''
copy a path (a file or folder)
to a destination.

determines if src is a file or folder
and calls appropriate function
(copy_file or copy_folder_recursively)
see those functions for details on
what they do.

src:
    String. absolute path of file or
    folder to copy
dest:
    String. absolute path of destination
    to copy to.
    in case where src is a file:
        dest can be either a file or a folder.
        if a file, will copy src to that
        filepath (i.e. cp src dest)
        if folder, will copy src INTO the
        folder.
    in case where src is a folder:
        dest must be a folder.
        see function declaration for
        'copy_folder_recursively' to see
        how dest is handled (it will get
        passed to that function as the dest
        option)
force:
    (only used when path is a file)
    boolean.
    if both path and dest are files, and
    dest file exists:
    if force is True, will overwrite dest
    with src.
    if force is False, will fail.
explode:
    (only used when path is a directory)
    boolean.
    if True, explodes contents of path
    directly into dest dir, rather than
    copying
    the source folder itself.
    i.e. src = a/b/c, dest=d/e/f
    if explode=True, the contents of
    folder "c" get copied directly into
    d/e/f
    if explode=False, the folder "c"
    itself gets copied info d/e/f
    (so you end up with d/e/f/c)
assume_dir:
    (only used when path is a file)
    boolean.
    See 'copy_file' function declaration
    for explanation.
    ** READ IT - IT'S NOT OBVIOUS **
glob_ignore:
    (only used when path is a directory)
    list of Strings - glob patterns -
    for files to ignore in the src directory
    to ignore.
    e.g. glob_ignore=["*.txt", "*.fs"]
    when doing the copy of src, would ignore
    any files with extensions .txt or .fs
'''


def copy_path(src, dest, force=False, explode=False, assume_dir=True, glob_ignore=[]):
    if not os.path.isabs(src) or not os.path.isabs(dest):
        raise Exception("ERROR io_utils:copy_path: "
                        "src or dest are not absolute")
    if not os.path.exists(src):
        raise Exception(("ERROR io_utils:copy_path: "
                         "src to copy doesn't exist! src: {}").format(src))

    if os.path.isdir(src):
        copy_folder_recursively(src, dest, explode, glob_ignore)
    elif os.path.isfile(src):
        copy_file(src, dest, force, assume_dir)
    else:
        raise Exception(("ERROR io_utils:copy_path: "
                         "src not file or dir according to python.. "
                         "src: {}").format(src))


'''
copy list of paths (can be files
or folders) to a destination.

paths:
    list of Strings.
    Absolute paths of files or
    directories to copy.

** remaining options, see
function declaration of 'copy_path'
for expalatnions **

'''


def copy_paths(paths, dest, force=False, explode=False, assume_dir=True, glob_ignore=[]):
    for path in paths:
        copy_path(path, dest, force, explode, assume_dir, glob_ignore)


'''
filepath: absolute path to a file.
Reads text content and returns as String
'''


def get_file_as_str(filepath):
    if not os.path.isabs(filepath):
        sys.exit(("ERROR: (io_utils): can't read {}, "
                  "path is not absolute!").format(filepath))
    if not os.path.exists(filepath):
        sys.exit(("ERROR: (io_utils): Can't read {}; "
                  "file does not exist!").format(filepath))

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
        sys.exit(("ERROR: (io_utils:write_str_to_file) "
                  "Output file not absolute! "
                  "(Output file: {})").format(filepath))

    if os.path.exists(filepath) and not force:
        sys.exit(("ERROR (io_utils:write_str_to_file): Output "
                  "file {} exists "
                  "(your script should call this function with "
                  "force=True)").format(filepath))
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
copy a file to a destination;

src:
    String. absolute path of file to copy
dest:
    String. absolute path to copy to.
    Can be either file or folder.

    if file: will copy file to this location.
    (if dest file already exists, will fail
    unless Force=True)

    if directory: will copy file into the
    directory. If dir doesn't exist,
    Will create it and any intermediary dirs
force:
    boolean
    if dest is a file and file exists:
    if force=True, will overwrist dest with src
    if force=False, will fail with message.
assume_dir:
    if dest doesn't exist, and no extension given,
    there's no way to determine whether dest
    intended as a directory or file (could be you
    want it to be a file with no extension).
    if this option is True, will assume you
    intended for dest to be a folder and will
    create it and then copy src into the folder.
    else will assume it's meant to be a file
    with no extension and will copy it to file

ex: copy_file("a/b/c.txt", "a/b/d.txt")
copies file a/b/c.txt to a/b/d.txt
'''


def copy_file(src, dest, force=False, assume_dir=True):
    if not os.path.isabs(src) or not os.path.isabs(dest):
        raise Exception("ERROR io_utils:copy_file: "
                        "src or dest are not absolute")
    if not os.path.exists(src):
        raise Exception("ERROR io_utils:copy_file: "
                        "src file doesn't exist! src: {}".format(src))
    # fail if dest exists and isn't a dir
    if not force and os.path.exists(dest) and not os.path.isdir(dest):
        raise FileExistsError("ERROR io_utils:copy_file: dest to copy to, {}, "
                              "already exists (to copy and overwrite, rerun "
                              "with force=True))".format(dest))
    # fail if dest is a dir but it contains of a file called src
    src_filename = os.path.basename(src)
    if not force and os.path.isdir(dest) and \
            os.path.exists(os.path.abspath(os.path.join(dest, src_filename))):
        raise FileExistsError("\n\nERROR (io_utils:copy_file)\n"
                              "Trying to copy file:\n\t"
                              "{}\nTo dest directory:\n\t{}\n"
                              "dest already contains a file named {}!\n"
                              "To overwrite the file, rerun with force=True"
                              .format(src, dest, src_filename))

    createPath(dest, assume_dir)

    '''
    if you ever change from using shutil.copy,
    make sure new method does what you claim in this function,
    ex., if dest is a dir, shutil.copy creates a file with basename
    of src and puts that in dest; if dest a filename just copies
    it directly there and overwrites if it exists
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
        raise Exception("ERROR io_utils:copy_files: dest dir "
                        "is not absolute! {}".format(dest))
    if os.path.exists(dest) and not os.path.isdir(dest):
        raise Exception("ERROR io_utils:copy_files: dest exists "
                        "is not a dir! {}".format(dest))
    if not os.path.exists(dest) and file_ext(dest):
        raise Exception("\n\nERROR io_utils:copy_files: dest doesn't "
                        "exist, but has a file extension.\n"
                        "Dest for this function must be a directory"
                        " (and then will copy all the files in 'files'"
                        " into that dir). Dest supplied:\n{}".format(dest))
    os.makedirs(dest, exist_ok=True)
    for file in files:
        copy_file(file, dest, force, True)


'''
Takes abs path to <src> dir and <dest> dir, and
cp -r <src> <dest>
overwrites <dest>/<src> if exists

Optional arg explode will explode the dir
in to dest, i.e.
cp -r <src>/. <dest>

glob_ignore:
    list of Strings: glob patterns for files
    to ignore.
    ex. glob_ignore=["*.txt", "*.fs"]
    would ignore any files with extensions
    .txt or .fs

Example:
if you have folder a/b/c
and you want to copy 'c' and contents to
path a/d/e/f,
  copy_folder_recursively('a/b/c', 'a/d/e/f')
results in:
    a/d/e/f/c
  copy_folder_recursively('a/b/c', a/d/e/f', explode=True)
results in
    contents of 'a/b/c' copied directly in to a/d/e/f
'''


def copy_folder_recursively(src, dest, explode=False, glob_ignore=[]):
    if not os.path.isabs(src) or not os.path.isabs(dest):
        sys.exit("ERROR (io_utils:copy_folder_recursively): "
                 "can't copy folder - either src or dest "
                 "is not absolute!")

    src_dir = src
    # need to get top level folder name to construct dest path
    # (i.e. if 'a/b/c' want 'c')
    # os.path.basename will return empty string if path ends in '/' char
    # so strip it off if its there
    if src_dir.endswith("/"):
        src_dir = src_dir[:-1]  # strips off last char of string

    src_foldername = os.path.basename(src_dir)
    dest_dir = dest
    if not explode:
        dest_dir = os.path.join(dest, src_foldername)
    dest_dir = os.path.abspath(dest_dir)

    '''
    switching from distutils to shutil
    so can specify glob patterns to ignore

    Note: dirs_exist_ok = True or it will fail
    if dest_dir exists

    example of glob patterns to copytree:
    https://docs.python.org/3/library/shutil.html#copytree-example
    '''
    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(*glob_ignore))


'''
copy_folders

dirpaths:
    List of Lists.
    Each contains: [PATH [GLOBLIST]]
    Where PATH is a directory to
    copy, and [GLOBLIST] is a list of
    Strings, representing glob patterns
    for paths to exclude during the copy
    operation for PATH.

destpath:
    String. Absolute path of
    directory to copy dirpaths to

general_globs:
    List of Strings representing glob
    patterns for paths to exclude in
    the copy operation for EVERY folder
    in dirpaths (in addition to any
    specific globs a folder in dirpaths
    may have)

explode:
    boolean. if true, the the contents
    of the directories in dirpaths
    will be copied directly into destpath
    (rather than copying the folders them
    selves)
'''


def copy_folders(dirpaths, destpath, general_globs=[], explode=False):

    common_err_prefix = "\n\nio_utils:copy_folders:"
    common_err_msg = "\n(dirpaths should be a list of lists. " \
                     "Each inner list should have format: " \
                     "[PATH, [GLOBLIST]], " \
                     "where PATH is the path of the directory " \
                     "to copy, and [GLOBLIST] is a list of globs " \
                     "for paths to exclude during the copy operation.)\n"

    '''
    Each inner list in 'dirpaths'
    represents a single directory
    to copy. Loop through 'dirpaths'
    and call 'copy_folder_recursively'
    on that dir, with relevant info.
    '''
    for dirpath_list in dirpaths:

        dirpath = ""
        globs = []

        # make sure it is a list
        if not type(dirpath_list) is list:
            raise Exception("{} one of the elements "
                            "in 'dirpaths' arg is NOT a list."
                            "{}"
                            "Problem item:\n{}"
                            .format(common_err_prefix, common_err_msg,
                                    str(dirpath_list)))
        if len(dirpath_list) == 2:
            # first is path, second (if any) is list of globs
            dirpath = dirpath_list[0]
            globs = dirpath_list[1]
            if type(globs) is list:
                # those are globs JUST for this directory;
                # add general globs to it (if any)
                globs.extend(general_globs)
            else:
                raise Exception("{} while looping through 'dirpaths' arg, "
                                "came across an inner list which DOES "
                                "have two items, however, the second item "
                                "is NOT a list."
                                "{}"
                                "Problem element:\n"
                                "  1. (the inner list itself):\n\t{}\n"
                                "  2. (2nd item in the inner list):\n\t{}\n"
                                .format(common_err_prefix, common_err_msg,
                                        str(dirpath_list), str(globs)))
        else:
            raise Exception("{} while looping through 'dirpaths' arg, "
                            "came across an inner list which does not "
                            "have two items."
                            "{}"
                            "Problem inner list:\n{}"
                            .format(common_err_prefix, common_err_msg,
                                    str(dirpath_list)))

        copy_folder_recursively(dirpath, destpath, explode, globs)


'''
Takes a filepath (either path to a file, or path to a directory).
If it's a file, creates parent directory recurisvely.
If it's a directory, creates entire dirpath.
returns True on success

file:
    String; the filepath to create

assume_dir:
    boolean
    if filepath has no extension and doesn't
    exist, there's ambiguity on if it's intended
    to be a dir, or a file with no extension.
    if assume_dir=True, will assume it's a
    a dir and will create the full path given
    by filepath.
    if assume_dir=False, will assume it's a file
    with no extension, and will only create the
    path, up to it's parent directory

Examples:
    createPath("a/b/c.txt")
        creates dirpath a/b
    createPath("a/b/c/d")
        creates dirpath a/b/c/d
    createPath("a/b/c/d", assume_dir=False)
        creates dirpath a/b/c

Note: if the filepath already exists, it simply returns.
'''


def createPath(filepath, assume_dir=True):
    if not os.path.isabs(filepath):
        raise Exception("\n\nio_utils:createPath: trying to "
                        "create directory path for {}, but "
                        "it's not an absolute path"
                        .format(filepath))

    if os.path.exists(filepath):
        return True
    else:
        path_to_create = filepath
        '''
        only create path up to filepath's
        containing dir if:
        (1) filepath specified a file (has file
        extension), or
        (2) no file extension, but
        assume_dir = False (meaning, essentially
        to assume it's a file with no extension)

        e.g. filepath = "a/b/c/d.txt"
        --> only create a/b/c/
        filepath = "a/b/c/d", assume_dir=False
        --> only create a/b/c
        (because you're assuming that
        "d" will be a file with no extension,
        that will live in a/b/c)
        '''
        if not assume_dir or file_ext(filepath):
            path_to_create = os.path.dirname(filepath)

        # if this ends up being filepath's
        # parent dir, it might exist
        # (only checked filepath didn't exist;
        # not parent)
        # so add exist_ok=True
        # or os.makedirs will fail
        os.makedirs(path_to_create, exist_ok=True)
        return True


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
        files = [f.name for f in os.scandir(folder) if f.is_file()]
    else:
        files = [f.path for f in os.scandir(folder) if f.is_file()]
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
        subfolders = [f.name for f in os.scandir(folder) if f.is_dir()]
    else:
        subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
    return subfolders
