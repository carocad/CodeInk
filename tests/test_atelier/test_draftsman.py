import os
import ast

import networkx
import astunparse
from networkx.readwrite import json_graph

from codeink.atelier import scientist
from codeink.atelier import draftsman
from codeink.parchment import pkginfo
from codeink.parchment import peephole
from codeink.atelier import secretary

def test_sketch_blocks():
    cwd = os.path.dirname(__file__)
    test_dir = os.path.dirname(cwd)
    pig_path = os.path.join(test_dir, 'guinea-pig')
    pig1 = os.path.join(pig_path, 'cage1', 'pig1.py')
    pig2 = os.path.join(pig_path, 'cage2', 'pig2.py')
    assistant = os.path.join(pig_path, 'lab_assistant.py')

    excluding = []
    dirs = list(pkginfo.get_directories(pig_path))
    modpaths = list(pkginfo.get_modules(dirs))
    modpaths = pkginfo.filter_modules(modpaths, excluding)
    if pkginfo.is_package(pig_path):
        dirs.append(os.path.dirname(pig_path))
    graph = draftsman.sketch_blocks(modpaths, dirs)

    answer = networkx.Graph()
    with open(pig1) as source:
        size1, color1 = scientist.get_size_color(source.read(), initsize=80)
    with open(pig2) as source:
        size2, color2 = scientist.get_size_color(source.read(), initsize=80)
    with open(assistant) as source:
        size_assist, color_assist = scientist.get_size_color(source.read(), initsize=80)
    answer.add_node(pig1, {'shape':'square', 'name':pig1, 'size':size1, 'color':color1})
    answer.add_node(pig2, {'shape':'square', 'name':pig2, 'size':size2, 'color':color2})
    answer.add_node(assistant, {'shape':'square', 'name':assistant, 'size':size_assist, 'color':color_assist})
    answer.add_node('python', {'shape':'circle', 'name':'Python', 'docstring':'Python builtin modules',
                               'filepath':'builtin', 'size':300, 'color':'hsl(207, 51%, 44%)'})
    answer.add_edge(pig2, pig1)
    answer.add_edge(assistant, 'python')
    answer.add_edge(assistant, pig1)
    answer.add_edge(assistant, pig2)

    assert networkx.is_isomorphic(answer, graph)

def test_sketch_footprint():
    cwd = os.path.dirname(__file__)
    test_dir = os.path.dirname(cwd)
    pig_path = os.path.join(test_dir, 'guinea-pig')
    pig1 = os.path.join(pig_path, 'cage1', 'pig1.py')
    pig2 = os.path.join(pig_path, 'cage2', 'pig2.py')
    assistant = os.path.join(pig_path, 'lab_assistant.py')

    rootpath = pkginfo.find_root_pkg(assistant)
    dirs = list(pkginfo.get_directories(rootpath))
    graph = draftsman.sketch_footprint(assistant, dirs)

    answer = networkx.Graph()
    with open(pig1) as source:
        size1, color1 = scientist.get_size_color(source.read(), initsize=80)
    with open(pig2) as source:
        size2, color2 = scientist.get_size_color(source.read(), initsize=80)
    with open(assistant) as source:
        size_assist, color_assist = scientist.get_size_color(source.read(), initsize=80)
    answer.add_node(pig1, {'shape':'square', 'name':pig1, 'size':size1, 'color':color1})
    answer.add_node(pig2, {'shape':'square', 'name':pig2, 'size':size2, 'color':color2})
    answer.add_node(assistant, {'shape':'square', 'name':assistant, 'size':size_assist, 'color':color_assist})
    answer.add_node('python', {'shape':'circle', 'name':'Python', 'docstring':'Python builtin modules',
                               'filepath':'builtin', 'size':300, 'color':'hsl(207, 51%, 44%)'})
    answer.add_edge(assistant, 'python')
    answer.add_edge(assistant, pig1)
    answer.add_edge(assistant, pig2)
    answer.add_edge(pig2, pig1)

    assert networkx.is_isomorphic(answer, graph)

def test_accusation():
    cwd = os.path.dirname(__file__)
    test_dir = os.path.dirname(cwd)
    pig_path = os.path.join(test_dir, 'guinea-pig')
    pig1 = os.path.join(pig_path, 'cage1', 'pig1.py')
    pig2 = os.path.join(pig_path, 'cage2', 'pig2.py')
    assistant = os.path.join(pig_path, 'lab_assistant.py')

    rootpath = pkginfo.find_root_pkg(pig1)
    dirs = list(pkginfo.get_directories(rootpath))
    modpaths = list(pkginfo.get_modules(dirs))
    modpaths = pkginfo.filter_modules(modpaths, [])
    graph = draftsman.sketch_accusation(pig1, modpaths, dirs)

    answer = networkx.Graph()
    with open(pig1) as source:
        size1, color1 = scientist.get_size_color(source.read(), initsize=80)
    with open(pig2) as source:
        size2, color2 = scientist.get_size_color(source.read(), initsize=80)
    with open(assistant) as source:
        size_assist, color_assist = scientist.get_size_color(source.read(), initsize=80)
    answer.add_node(pig1, {'shape':'square', 'name':pig1, 'size':size1, 'color':color1})
    answer.add_node(pig2, {'shape':'square', 'name':pig2, 'size':size2, 'color':color2})
    answer.add_node(assistant, {'shape':'square', 'name':assistant, 'size':size_assist, 'color':color_assist})
    answer.add_edge(assistant, pig1)
    answer.add_edge(pig2, pig1)

    assert networkx.is_isomorphic(answer, graph)

def test_profile():
    cwd = os.path.dirname(__file__)
    test_dir = os.path.dirname(cwd)
    pig_path = os.path.join(test_dir, 'guinea-pig')
    pig1 = os.path.join(pig_path, 'cage1', 'pig1.py')
    module_name = 'pig1'

    graph = draftsman.sketch_profile(pig1)

    answer = networkx.Graph()
    with open(pig1) as source:
        code = source.read()
        size1, color1 = scientist.get_size_color(code, initsize=80)
        modtree = ast.parse(code, module_name)
    answer.add_node(module_name, {'shape':'square', 'name':pig1, 'size':size1, 'color':color1})

    function = list(peephole.get_functions(modtree))[0]
    funkcode = astunparse.unparse(function)
    size, color = scientist.get_size_color(funkcode)
    funkname = secretary.make_scoped_name(module_name, function.name)
    funkinfo = {'shape':'triangle-up' ,'name':funkname, 'size':size, 'color':color}
    answer.add_node(funkname, funkinfo)
    answer.add_edge(module_name, funkname)

    classdef = list(peephole.get_classes(modtree))[0]
    classcode = astunparse.unparse(classdef)
    size, color = scientist.get_size_color(classcode)
    classname = secretary.make_scoped_name(module_name, classdef.name)
    classinfo = {'shape':'diamond' ,'name':classname, 'size':size, 'color':color}
    answer.add_node(classname, classinfo)
    answer.add_edge(module_name, classname)

    method1 = list(peephole.get_functions(classdef))[0]
    method1code = astunparse.unparse(method1)
    size, color = scientist.get_size_color(method1code)
    methodname = secretary.make_scoped_name(classname, method1.name)
    methodinfo = {'shape':'triangle-down' ,'name':methodname, 'size':size, 'color':color}
    answer.add_node(methodname, methodinfo)
    answer.add_edge(classname, methodname)

    method2 = list(peephole.get_functions(classdef))[1]
    method2code = astunparse.unparse(method2)
    size, color = scientist.get_size_color(method2code)
    methodname = secretary.make_scoped_name(classname, method2.name)
    methodinfo = {'shape':'triangle-down' ,'name':methodname, 'size':size, 'color':color}
    answer.add_node(methodname, methodinfo)
    answer.add_edge(classname, methodname)

    assert networkx.is_isomorphic(answer, graph)
