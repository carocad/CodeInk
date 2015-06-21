""" functions in charge of creating graph objects and populating
them with the requested information"""

import os
import ast
import modulefinder

import networkx
import astunparse

from codeink.atelier import secretary
from codeink.atelier import scientist
from codeink.parchment import peephole

def sketch_blocks(modulepaths, pkg_dirs):
    """Creates a graph of all the modules in `modulepaths` that are related to each other by their
    imports. The directories used to resolve an import is `pkg_dirs`

    Args:
        modulepaths (List[str]): list of modules filepaths to analyze.
        pkg_dirs (List[str]): list of directories used to resolve the imports
    Returns:
        networkx.Graph: graph of the modules as nodes with their imports as edges.
    """
    attributes = init(pkg_dirs)
    graph = attributes['graph']
    Python = 'python'
    graph.add_node(Python, attributes[Python])
    for filepath in modulepaths:
        # bug - if the finder is not reinitialized, the previous modules.values()
        #       are kept, thus been useless
        finder = modulefinder.ModuleFinder(path=pkg_dirs)
        print('processing:\t', filepath)
        # Calculate complexity and maintainability indexes
        with open(filepath) as source:
            size, color = scientist.get_size_color(source.read(), initsize=80)
        # Insert current module info
        module_info = {'shape':'square', 'name':filepath, 'size':size, 'color':color}
        graph.add_node(filepath, module_info)
        # Find module imports
        finder.run_script(filepath)
        for edge in scientist.compute_edges(filepath, Python, finder.modules.values(),
                                            finder.badmodules.keys()):
            graph.add_edge(*edge)
    return graph

def sketch_footprint(absfilepath, project_dirs):
    """Creates a graph of all the modules related to `absfilepath` by his
    imports. The directories used to resolve an import are `project_dirs`.
    Note that the relations are recursive,i.e. the modules imported by `absfilepath`
    as well as modules imported by those other modules, are included in the graph
    until no more modules are left to analyze.

    Args:
        absfilepath (str): filepath of the module to analyze.
        project_dirs (List[str]): list of directories used to resolve the imports
    Returns:
        networkx.Graph: graph of the modules as nodes with their imports as edges.
    """
    attributes = init(project_dirs)
    graph = attributes['graph']
    Python = 'python'
    graph.add_node(Python, attributes[Python])
    modules_to_check = [absfilepath]
    modules_checked = []
    while modules_to_check:
        modulepath = modules_to_check.pop()
        if modulepath in modules_checked:
            continue
        modules_checked.append(modulepath)
        print('processing:\t', modulepath)
        finder = modulefinder.ModuleFinder(path=project_dirs)
        # Calculate complexity and maintainability indexes
        with open(modulepath) as source:
            size, color = scientist.get_size_color(source.read(), initsize=80)
        # Insert current module info
        contour = 'square' if modulepath != absfilepath else 'cross'
        module_info = {'shape':contour, 'name':modulepath, 'size':size, 'color':color}
        graph.add_node(modulepath, module_info)
        # Find module imports, ignore badmodules
        finder.run_script(modulepath)
        for edge in scientist.compute_edges(modulepath, Python, finder.modules.values(),
                                            finder.badmodules.keys()):
            graph.add_edge(*edge)
        for module in finder.modules.values():
            if scientist.include_module(module):
                modules_to_check.append(module.__file__)
    return graph

def sketch_accusation(targetpath, modulepaths, project_dirs):
    """Creates a graph of all the modules in `modulepaths` that import
    the module at `targetpath`. The directories used to resolve an import are `project_dirs`

    Args:
        targetpath (str): filepath of the module whose import status is being checked.
        modulepaths (List[str]): list of modules filepaths to check for imports.
        project_dirs (List[str]): list of directories used to resolve the imports
    Returns:
        networkx.Graph: graph of the module as nodes with their imports as edges.
    """
    graph = networkx.Graph()
    # Calculate complexity and maintainability
    with open(targetpath) as source:
        size, color = scientist.get_size_color(source.read(), initsize=80)

    # Insert target module info
    target_info = {'shape':'cross' ,'name':targetpath, 'size':size, 'color':color}
    graph.add_node(targetpath, target_info)
    for modulepath in modulepaths:
        print('processing:\t', modulepath)
        finder = modulefinder.ModuleFinder(path=project_dirs)
        finder.run_script(modulepath)
        for module in finder.modules.values():
            if (scientist.include_module(module)
            and module.__file__ == targetpath):
                with open(modulepath) as source:
                    size, color = scientist.get_size_color(source.read(), initsize=80)
                module_info = {'shape':'square' ,'name':modulepath, 'size':size, 'color':color}
                graph.add_node(modulepath, module_info)
                graph.add_edge(modulepath, targetpath)

    return graph

def sketch_profile(absfilepath):
    """Creates a graph of all the functions, classes and methods defined in the module at
    `absfilepath`.

    Args:
        absfilepath (str): absolute filepath of the module whose definition are
          being checked.
    Returns:
        networkx.Graph: graph of the functions and classes as nodes with their scopes
          as edges.
    """
    graph = networkx.Graph()
    module_name = os.path.basename(absfilepath)[:-3] # take the .py away
    with open(absfilepath) as source:
        code = source.read()
        size, color = scientist.get_size_color(code, initsize=80)
        modtree = ast.parse(code, module_name)
    # Insert target module info
    module_info = {'shape':'square', 'name':module_name, 'size':size, 'color':color}
    graph.add_node(module_name, module_info)
    for function in peephole.get_functions(modtree):
        funkcode = astunparse.unparse(function)
        size, color = scientist.get_size_color(funkcode)
        funkname = secretary.make_scoped_name(module_name, function.name)
        funkinfo = {'shape':'triangle-up' ,'name':funkname, 'size':size, 'color':color}
        graph.add_node(funkname, funkinfo)
        graph.add_edge(module_name, funkname)
    for classobj in peephole.get_classes(modtree):
        classcode = astunparse.unparse(classobj)
        size, color = scientist.get_size_color(classcode)
        classname = secretary.make_scoped_name(module_name, classobj.name)
        classinfo = {'shape':'diamond' ,'name':classname, 'size':size, 'color':color}
        graph.add_node(classname, classinfo)
        graph.add_edge(module_name, classname)
        for method in peephole.get_functions(classobj):
            methodcode = astunparse.unparse(method)
            size, color = scientist.get_size_color(methodcode)
            methodname = secretary.make_scoped_name(module_name, classobj.name,
                                                    method.name)
            methodinfo = {'shape':'triangle-down' ,'name':methodname, 'size':size, 'color':color}
            graph.add_node(methodname, methodinfo)
            graph.add_edge(classname, methodname)

    return graph

def init(dirs):
    attributes = {}
    # Initialize a graph object
    attributes['graph'] = networkx.Graph()
    # Create the most basic node
    attributes['python'] = { 'shape':'circle', 'name':'Python',
                             'docstring':'Python builtin modules',
                             'filepath':'builtin', 'size':300,
                             'color':'hsl(207, 51%, 44%)'} # color = dark blue
    #attributes['finder'] = modulefinder.ModuleFinder(path=dirs)
    return attributes
