
import math
import modulefinder
import os
import networkx
import radon.metrics
from nicolas.atelier import secretary

def sketch_blocks(project_modules, pkg_dirs):
	# Initialize a graph object
	graph = networkx.Graph()
	# Create the most basic node
	Python = 'Python'
	graph.add_node(hash(Python), type='master', name=Python,
				  docstring='Python builtin modules', filepath='builtin',
				  size=10, color='#004C00')

	finder = modulefinder.ModuleFinder(path=pkg_dirs)
	for filepath in project_modules:
		print('processing:\t', filepath)
		# Calculate complexity and maintainability indexes
		size, color = check_complexity(filepath)
		# Insert current module info
		module_info = {'name':filepath, 'size':size, 'color':color}
		graph.add_node(hash(filepath), module_info)
		# Find module imports
		finder.run_script(filepath)
		for module in finder.modules.values():
			if module.__file__ is not None and not module.__file__.endswith('__init__.py') and (
			   filepath != module.__file__) and module.__name__ != '__main__':
				# project module but no package
				graph.add_edge(hash(filepath), hash(module.__file__))
			else: # builtin modules
				graph.add_edge(hash(filepath), hash(Python))
		if finder.badmodules.values():
			graph.add_edge(hash(filepath), hash(Python))

		#graph.add_star([module] + list(imports))
		#graph.add_node(module, impno=len(imports))
	return graph

def check_complexity(filepath):
	maintainability = 0
	size = 3 # minimum size
	with open(filepath) as source:
		halstead, cyclom, lloc, pcom = radon.metrics.mi_parameters(source.read(), count_multi=False)
		maintainability = radon.metrics.mi_compute(halstead, cyclom, lloc, pcom)
		size += math.sqrt(cyclom)

	rgb = secretary.value_to_RGB(maintainability)
	color = secretary.rgb_to_hex(rgb)
	return size, color
