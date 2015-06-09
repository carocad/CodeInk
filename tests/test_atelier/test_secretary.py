import os

from codeink.atelier import secretary
from codeink.parchment import peephole

def get_test_filepath():
    # get out of the test-secretary directories
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    guineapig_path = os.path.join(parent_dir, 'guinea-pig',
                                  'cage1', 'pig1.py')
    return guineapig_path

def test_get_module_info():
    guineapig_path = get_test_filepath()
    tree = peephole.parse(guineapig_path)
    module_info = {'type':'module', 'name':'pig1',
                   'docstring':'pig1 module', 'filepath':guineapig_path}
    assert module_info == secretary.get_module_info(tree, guineapig_path)

def test_function_info():
    guineapig_path = get_test_filepath()
    tree = peephole.parse(guineapig_path)
    funk = list(peephole.get_functions(tree))[0] # unique function in the file
    funk_info = {'type':'function', 'name':'foo', 'docstring':'foo function',
                 'filepath':guineapig_path, 'lineno':3}
    assert funk_info == secretary.get_function_info(funk, guineapig_path)

def test_get_class_info():
    guineapig_path = get_test_filepath()
    tree = peephole.parse(guineapig_path)
    classdef = list(peephole.get_classes(tree))[0] # unique function in the file
    class_info = {'type':'class', 'name':'bar', 'docstring':'None',
                  'filepath':guineapig_path, 'lineno':7 }
    assert class_info == secretary.get_class_info(classdef, guineapig_path)

def test_value_to_HSL():
    # test red value
    red = 0 # min
    ## val, fix, fix
    assert (0, 90, 40) == secretary.value_to_HSL(red)
    # test green value
    green = 100 # max
    assert (120, 90, 40) == secretary.value_to_HSL(green)

def test_hsl_to_str():
    green = 100 # max
    answer = 'hsl(120, 90%, 40%)'
    hsl = secretary.value_to_HSL(green)
    assert answer == secretary.hsl_to_str(*hsl)

def test_make_scoped_name():
    child = 'foo'
    parent = 'bar'
    grandparent = 'lalo'
    answer = grandparent + '.' + parent + '.' + child
    assert answer == secretary.make_scoped_name(grandparent, parent, child)
