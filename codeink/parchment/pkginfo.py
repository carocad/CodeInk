"""Provides general information regarding packages and modules
as well as general utility functions to deal with them
"""

import os
import pkgutil
import fnmatch

def get_directories(dirpath, extension='.py'):
    """ recursively get all subdirectories including `dirpath`
    that contain files with the requested extension.

    Args:
        dirpath(str): directory path to be use as start point;
            both absolute and relative path are supported.
        extension(Optional[str]): file extension to check files against.
    Yields:
        str: path of a directory containing files with the
            requested extension.
    """
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if fnmatch.fnmatch(file, '*' + extension):
                yield root
                break

def is_package(absdirpath):
    """ checks if a directory is in fact a python package.

    Args:
        absdirpath (str): directory path whose package status
          is being tested
    Returns:
        bool: True if the directory is a package, false otherwise.
    """
    parent_dir = os.path.dirname(absdirpath)
    pkg_name = os.path.basename(absdirpath)
    for root, name, ispkg in pkgutil.iter_modules([parent_dir]):
        if ispkg and name == pkg_name:
            return True
    return False

def get_modules(directories):
    """ get all the modules present in `directories`

    Args:
        directories (list): list of directories where the modules
          may lay in.
    Yields:
        str: absolute filepath of a module
    """
    for root, name, ispkg in pkgutil.iter_modules(directories):
        if hasattr(root, 'path') and not ispkg:
            yield os.path.join(root.path, name + '.py')

def filter_modules(modpaths, patterns):
    """filter away modules that match a specific name pattern.
    Note: since modpaths are full filepaths, the name pattern
    MUST be specified for the path itself, as opposed to only
    the filename.

    Args:
        modpaths (List[str]): list of absolute modules filepath to
          filter
        patterns (List[str]): list of strings with Unix shell-style
          wildcards.
    Returns:
        List[str]: list of absolute filepaths that didnt match
          any pattern.
    """
    for pattern in patterns:
        modpaths = [ filepath for filepath in modpaths
                     if not fnmatch.fnmatch(filepath, pattern) ]
    return modpaths

def find_root_pkg(absfilepath):
    """find the root package of a specific file, i.e. the most
    upper directory that is considered a package.

    Args:
        absfilepath (str): absolute filepath of the module whose
          root package is being searched.
    Returns:
        str: absolute filepath of the found root package.
    """
    rootpath = os.path.dirname(absfilepath)
    ispkg = is_package(rootpath)
    while ispkg:
        rootpath = os.path.dirname(rootpath)
        ispkg = is_package(rootpath)
    return rootpath
