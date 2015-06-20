"""general unrelated utilities that save time and are nice encapsulations"""

import os

from codeink.parchment import peephole

def get_module_info(tree, absfilepath):
    """ put a modules general info into a dictionary

    Args:
        tree (ast.Module): parsed ast module tree
        absfilepath (str): absolute filepath of the module
    Returns:
        dict: dictionary with selected information items
    """
    _name = os.path.basename(absfilepath)[:-3] # strip the .py from filepath
    _doc = peephole.get_attr(tree, 'doc')
    _path = absfilepath
    return {'type':'module', 'name':_name, 'docstring':_doc, 'filepath':_path}

def get_function_info(func, path):
    """ put a function general info into a dictionary

    Args:
        func (ast.FunctionDef): function definition instance
          as defined in AST
        path (str): absolute filepath of the module where the
          function is defined
    Returns:
        dict: dictionary with selected information items
    """
    _name = func.name
    _doc = peephole.get_attr(func, 'doc')
    _path = path
    _lineno = func.lineno
    return {'type':'function', 'name':_name, 'docstring':_doc,
            'filepath':_path, 'lineno':_lineno}

def get_class_info(classDef, path):
    """ put a class general info into a dictionary

    Args:
        tree (ast.ClassDef): class definition instance as
          defined in AST
        path (str): absolute filepath of the module where the
          class is defined
    Returns:
        dict: dictionary with selected information items
    """
    _name = classDef.name
    _doc = peephole.get_attr(classDef, 'doc')
    _path = path
    _lineno = classDef.lineno
    return {'type':'class', 'name':_name, 'docstring':_doc,
            'filepath':_path, 'lineno':_lineno}

def value_to_HSL(value):
    """ Convert a value ranging from 0 to 100 into a color
    ranging from red to green using the HSL colorspace.

    Args:
        value (int): integer betwee 0-100 to be converted.
    Returns:
        Tuple[int]: hue, saturation and lightnes corresponding
          to the converted value.
    """
    # max(value) = 100
    hue = int(value * 1.2) # 1.2 = green, 0 = red
    saturation = 90
    lightness = 40
    return (hue, saturation, lightness)

def hsl_to_str(hue, sat, light):
    """ Convert an HSL color value into a string.

    Args:
        hue (int): value between 0-360
        sat (int): value between 0-100
        light (int): value between 0-100
    Returns:
        str: string representation of the HSL tuple. Note that
          the hue is an integer, whereas the saturation and
          lightness are porcentages.
    """
    return 'hsl({h}, {s}%, {l}%)'.format(h=hue, s=sat, l=light)

def make_scoped_name(*args):
    """ Convert a series of strings into a single string
    representing joined by points. This convertion represents
    Pythons scope convention.i.e. pkg.subpkg.module

    Args:
        *ags: list of string. The strings will
          joined in FIFO order.
    Returns:
        str: string-scope representation.
    """
    return '.'.join(args)
