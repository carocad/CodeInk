
import os
import modulefinder

from codeink.atelier import scientist
from codeink.parchment import pkginfo

def test_check_complexity():
	parent_dir = os.path.dirname(os.path.dirname(__file__))
	guineapig_path = os.path.join(parent_dir, 'guinea-pig',
								  'cage2', 'pig2.py')
	default = 80
	#empty file --> complexity = 1
	answer = (default+1, 'hsl(120.0, 90%, 40%)')
	assert answer == scientist.check_complexity(guineapig_path)

def test_compute_edges():
	parent_dir = os.path.dirname(os.path.dirname(__file__))
	guineapig_path = os.path.join(parent_dir, 'guinea-pig')
	master_module = os.path.join(parent_dir, 'guinea-pig', 'lab_assistant.py')
	pig1_path = os.path.join(parent_dir, 'guinea-pig', 'cage1', 'pig1.py')

	dirs = list(pkginfo.get_directories(guineapig_path, '.py'))
	finder = modulefinder.ModuleFinder(path=dirs)
	finder.run_script(master_module)
	base = 'mammal'
	edges = set(scientist.compute_edges(master_module, base, finder.modules.values(),
										 finder.badmodules.keys()))
	for edge in edges:
		print(edge)
	answer = set([(master_module, base),
				  (master_module, pig1_path)])
	assert answer == edges

