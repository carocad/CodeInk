import os

import networkx
from networkx.readwrite import json_graph

from codeink.atelier import scientist
from codeink.atelier import draftsman
from codeink.parchment import pkginfo

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
    print(rootpath)
    print(dirs)
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
