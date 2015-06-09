""" parses a python module and fetches classes, functions and import statements definitions.

    * Copyright (c) 2015 Camilo Roca, carocad@unal.edu.co
"""

import ast
import astunparse
import copy
import textwrap

def parse(path):
    """parse a file at path and returns an AST tree structure

    Args:
        path (str): filepath of the file to parse
    Returns:
        ast.Module: ast tree of the parsed file
    """

    with open(path) as source_code:
        return ast.parse(source_code.read(), path)

def get_classes(node):
    """get the class definitions inside node

    Args:
        node (ast.AST): node containing a `body` attribute.
    Returns:
        ast.ClassDef: class definition instance present in the node body.
    """
    return filter( (lambda child: isinstance(child, ast.ClassDef)),  node.body)

def get_functions(node):
    """get the function definitions inside node

    Args:
        node (ast.AST): node containing a `body` attribute.
    Returns:
        ast.FunctionDef: function definition instance present in the node body.
    """
    return filter( (lambda child: isinstance(child, ast.FunctionDef)),  node.body)

def get_imports(node):
    """get the import definitions inside node

    Args:
        node (ast.AST): node containing a `body` attribute.
    Returns:
        ast.Import: import definition instance present in the node body.
    """
    return filter( (lambda child: isinstance(child, ast.Import)), node.body)

def get_importsFrom(node):
    """get the import from definitions inside node

    Args:
        node (ast.AST): node containing a `body` attribute.
    Returns:
        ast.ImportFrom: import_from definition instance present in the node body.
    """
    return filter( (lambda child: isinstance(child, ast.ImportFrom)), node.body)

def get_attr(node, name):
    """get the attribute of node or None if the attribute doesn't exist

    Args:
        node (ast.AST): node whose attribute is going to be check.
        name (str): name of the attribute whose existence is being tested.
    Returns:
        str: in case the docstring was requested.
        ast.AST: in case the requested attribute is an instance of AST.
        None: if the attibute was not found.
        object: any type that the attribute may have.
    """
    if name == 'doc':
        return str(ast.get_docstring(node, clean=True))
    if hasattr(node, name):
        return getattr(node, name)
