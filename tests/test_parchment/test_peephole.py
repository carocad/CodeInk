
import os
import ast

from codeink.parchment import peephole

def test_parse():
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    pig1_path = os.path.join(parent_dir, 'guinea-pig', 'cage1', 'pig1.py')
    tree = peephole.parse(pig1_path)
    assert ast.Module == type(tree)
    assert 'pig1 module' == peephole.get_attr(tree, 'doc')

def test_get_classes_and_functions():
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    pig1_path = os.path.join(parent_dir, 'guinea-pig', 'cage1', 'pig1.py')
    tree = peephole.parse(pig1_path)

    bar_class = list(peephole.get_classes(tree))[0]
    assert ast.ClassDef == type(bar_class)
    assert 'bar' == peephole.get_attr(bar_class, 'name')
    assert 7 == peephole.get_attr(bar_class, 'lineno')

    foo_funct = list(peephole.get_functions(tree))[0]
    assert ast.FunctionDef == type(foo_funct)
    assert 'foo' == peephole.get_attr(foo_funct, 'name')
    assert 3 == peephole.get_attr(foo_funct, 'lineno')
