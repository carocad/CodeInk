
import os
import modulefinder

from codeink.atelier import scientist
from codeink.parchment import pkginfo

def test_get_size_color():
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    guineapig_path = os.path.join(parent_dir, 'guinea-pig', 'cage2', 'pig2.py')
    default = 80

    answer = (default+1, 'hsl(120, 90%, 40%)')
    with open(guineapig_path) as test_source:
        assert answer == scientist.get_size_color(test_source.read(), initsize=default)

def test_compute_edges():
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    guineapig_path = os.path.join(parent_dir, 'guinea-pig')
    master_module = os.path.join(parent_dir, 'guinea-pig', 'lab_assistant.py')
    pig1_path = os.path.join(parent_dir, 'guinea-pig', 'cage1', 'pig1.py')
    pig2_path = os.path.join(parent_dir, 'guinea-pig', 'cage2', 'pig2.py')

    dirs = list(pkginfo.get_directories(guineapig_path, '.py'))
    finder = modulefinder.ModuleFinder(path=dirs)
    finder.run_script(master_module)
    base = 'mammal'
    edges = set(scientist.compute_edges(master_module, base, finder.modules.values(),
                                        finder.badmodules.keys()))
    answer = set([(master_module, base),
                  (master_module, pig1_path),
                  (master_module, pig2_path)])
    assert answer == edges

