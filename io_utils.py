import os
import sys
import shutil

ENC = 'utf-8'


def absolute(path, relTo):
    """
    Makes a filepath absolute (and normalizes path separators).

    :param str path: path to make absolute
    :param str relTo: if path is relative, creates
        the abs path relative to this path.
    :return: str. the normalized, absolute path.
    :example:
        absolute("../b.txt", "C:\\Users\\Boris\\Desktop")
        returns: "C:\\Users\\Boris\\b.txt"
    """
    if not path:
        raise Exception("\n\nERROR: io_utils:absolute: "
                        "Path to convert to absolute is "
                        "empty or None.\nPath: {}"
                        .format(path))
    if not os.path.isabs(path):
        if not os.path.isabs(relTo):
            raise Exception("\n\nERROR: io_utils:absolute: "
                            "This function takes a path, and "
                            "if that path is not absolute, it "
                            "forms the absolute value of that "
                            "path relative some other path.\n"
                            "Issue: Path passed was not absolute, "
                            "but path to evaluate it from is "
                            "not aboslute either!\n\n"
                            "Path:\n{}\n\n"
                            "Path to evaluate it relative from:\n{}"
                            .format(path, relTo))
        path = os.path.abspath(os.path.join(relTo, path))
    # normpath normalizes in case Unix + Windows separators
    return os.path.normpath(path)


def copy_file(src, dest, force=False, assume_dir=True):
    """
    copy a file to a destination (either a file or a dir)

    :param str src: abs path of file to copy
    :param str dest: abs path for destination
        dest can be either file or directory.
        if dir: copy src into dest. If dir
        doesn't exist, will create it and any
        intermediary dirs.
    :param boolean force: for case where dest is
        a file, overwrite if file already exists
    :param boolean assume_dir: assume dest is a dir
        in the case dest doesn't exist, and no ext given
        (see above for how 'dest' works when dest is a dir)
    :example:
        copy_file("a/b/c.txt", "a/b/d.txt")
        copies file a/b/c.txt to a/b/d.txt
    """
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


def copy_files(files, dest, force=False):
    """
    copy a list of files to a dest folder

    :param list[str] files: list of abs paths ofr files to copy
    :param str dest: abs path of dest folder to copy files to
    :return: None
    """

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


def copy_folder_recursively(src, dest, explode=False, glob_ignore=[]):
    """
    recursively copies a directory INTO a dest dir.
    essentially:
        cp -r <src> <dest>
        (overwrites <dest>/<src> if exists)

    :param str src: abs path to src dir
    :param str dest: abs path to dest dir to copy src INTO
    :param boolean explode: optional. explode CONTENTS of
        src into dest (rather than copying src itself into dest)
    :param list[str] glob_ignore: optional. glob patterns for
        files in src to ignore while copying.
        ex. glob_ignore=["*.txt", "*.fs"]
        will not copy any .txt or .fs files in src
    :return: None
    :example:
        copy_folder_recursively('a/b/c', 'a/d/e/f')
            results in: a/d/e/f/c
        copy_folder_recursively('a/b/c', a/d/e/f', explode=True)
            results in: contents of 'c' copied directly in to a/d/e/f
    """

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


def copy_folders(dirpaths, destpath, general_globs=[], explode=False):
    """
    copy multiple folders into a destination directory.

    :param list[list] dirpaths: the list of src dirs to copy.
        Each inner list is: [path, [GLOBLIST]] where
        path is a src dir to copy, and GLOBLIST
        is list[str], a list of glob patterns for files
        to exclude when copying path.
    :param str destpath: abs pat of dir to copy src dirs into
    :param list[str] general_globs: optional. list of glob
        patterns to apply to ALL src dirs for ignoring files
    :param boolean explode: explode contents of the src dirs
        directly into destpath (rather than copying the folders
        themselves into destpath)
    """

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


def copy_path(src, dest, force=False, explode=False, assume_dir=True,
              glob_ignore=[]):
    """
    copy a file or directory to a destination

    :param str src: abs path of file or folder to copy
    :param str dest: abs path of dest to copy to
        if src is a file:
            dest can be either file or folder.
            if a file, will copy src to that
            filepath (i.e. cp src dest)
            if folder, will copy src INTO dest.
        if src is a folder:
            dest must be a folder.
            see function declaration for
            'copy_folder_recursively' to see
            how dest is handled (it will get
            passed to that function as the dest
            option)
    :param boolean force: overwrite if dest exists.
    :param boolean explode: explode contents of src into
        dest, rather than copying the source folder itself.
        (only used when src is a directory)
        i.e. src=a/b/c, dest=d/e/f, (and both c and f are dirs)
        if explode=True, contents of "c" copied directly into d/e/f
        if explode=False, "c" itself gets copied info d/e/f
        (so you end up with d/e/f/c)
    :param boolean assume_dir:
        (only used when src is a file)
        See 'copy_file' function for explanation.
        ** READ IT - IT'S NOT OBVIOUS **
    :param list[str] glob_ignore: list of glob pattersn
        of files to ignore in src dir when copying.
        (only used when src is a directory)
        e.g. glob_ignore=["*.txt", "*.fs"]
        when copying src, dont files with extensions .txt or .fs
    """
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


def copy_paths(paths, dest, force=False, explode=False, assume_dir=True,
               glob_ignore=[]):
    """
    copy list of paths -- files or folders -- to a destination.
    :param list[str] paths: abs paths of files or dirs to copy
    -- for remaining options, see 'copy_path' function --
    """
    for path in paths:
        copy_path(path, dest, force, explode, assume_dir, glob_ignore)


def createPath(filepath, assume_dir=True):
    """
    Create a path on the local filesystem if it doesn't
    already exist.

    :param str file: filepath to create. can be file or dir.
        if file, will create path up to PARENT dir (not the
        file itself). If dir, will create the entire path.
    :param boolean assume_dir: optional. assume filepath is
        a dir, if there's no extension and path doesn't exist.
    :return: True on success, or if filepath already exists.

    examples:
        createPath("a/b/c.txt")
            creates dirpath a/b
        createPath("a/b/c/d")
            creates dirpath a/b/c/d
        createPath("a/b/c/d", assume_dir=False)
            creates dirpath a/b/c

    Note: if the filepath already exists, it simply returns.
    """
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


def file_ext(path):
    """
    return file extension from a path
    :param str path: path to get file ext from
    :return: str. the file extension (if file
        has no extension, returns "")
    :example:
        file_ext("a.txt")
            returns "txt"
        file_ext("b")
            returns ""
    """
    file_ext = os.path.splitext(path)[1]
    # remove . char from extension
    if file_ext:
        return file_ext[1:]
    return ""


def get_file_as_str(filepath):
    """
    return file contents of a file as a string
    :param str filepath: abs path to a file
    """
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


def list_files(folder, names=False):
    """
    Return list of files in a directory.

    :param str folder: name of folder to list files in
        Does not need to be abspath.
        if rel. path, should be be rel dir
        where script that imported this script
        is being called.
        e.g.: script a.py in dir /a/b/c/ imports io_utils and calls
        list_subdirs; you call a.py from /a/b/;
        the rel path to 'folder' should be rel /a/b/
    :param boolean names: optional. If True, return names of the
        files. If False, returns abs. paths to the files.
    :return: list[str]. files in the folder.
        if names=True - only returns filenames
        if names=False - abs paths to the filenames
    """

    # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    # (answer by gahooa)
    files = []
    if names:
        files = [f.name for f in os.scandir(folder) if f.is_file()]
    else:
        files = [f.path for f in os.scandir(folder) if f.is_file()]
    return files


def list_subdirs(folder, names=False):
    """
    return list of subdirs in a directory (not recursive)

    :param str folder: name of folder to get subdirs of.
        Does not need to be abspath.
        If rel, should be rel dir where script that imported
        this script is being called
        e.g.: if a.py in /a/b/c/ imports io_utils and calls
        list_subdirs; you call a.py from /a/b/;
        the rel path to 'folder' should be rel /a/b/
    :param boolean names: optional. if True, only return names
        of the dirs (else it returns abs paths to the dirs)
    :return: list[str]: the paths to immediate subdirs in folder
        (if names=True, will be just names of the subdirs;
        if names=False, will be abs paths to the subdirs)
    """

    # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    # (answer by gahooa)
    subfolders = []
    if names:
        subfolders = [f.name for f in os.scandir(folder) if f.is_dir()]
    else:
        subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
    return subfolders


def write_str_to_file(string, filepath, force):
    """
    writes a string to a file
    :param str string: the data to write to the file
    :param str filepath: abs path to write file to
    :param boolean force: overwrite if filepath exists
    """
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
