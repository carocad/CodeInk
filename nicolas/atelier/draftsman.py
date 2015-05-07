
import math
import modulefinder
import os
import networkx
import radon.metrics
from nicolas.atelier import secretary

def sketch_blocks(modulepaths, pkg_dirs):
	attributes = init(pkg_dirs)
	finder = attributes['finder']
	graph = attributes['graph']
	Python = 'python'
	graph.add_node(hash(Python), attributes[Python])
	for filepath in modulepaths:
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
				# project module but not package
				graph.add_edge(hash(filepath), hash(module.__file__))
			else: # builtin modules
				graph.add_edge(hash(filepath), hash(Python))
		if finder.badmodules.values():
			graph.add_edge(hash(filepath), hash(Python))
	return graph

def sketch_footprint(filepath, project_dirs):
	attributes = init(project_dirs)
	finder = attributes['finder']
	graph = attributes['graph']
	Python = 'python'
	graph.add_node(hash(Python), attributes[Python])
	modules_to_check = [filepath]
	modules_checked = []
	while modules_to_check:
		modulepath = modules_to_check.pop()
		if modulepath in modules_checked:
			continue
		modules_checked.append(modulepath)
		print('processing:\t', modulepath)
		print('size: ', len(modules_to_check))
		# Calculate complexity and maintainability indexes
		size, color = check_complexity(modulepath)
		# Insert current module info
		module_info = {'name':modulepath, 'size':size, 'color':color}
		graph.add_node(hash(modulepath), module_info)
		# Find module imports
		finder.run_script(modulepath)
		for module in finder.modules.values():
			if module.__file__ is not None and not module.__file__.endswith('__init__.py') \
				and (filepath != module.__file__) and module.__name__ != '__main__':
				# project module but not package
				graph.add_edge(hash(modulepath), hash(module.__file__))
				modules_to_check.append(module.__file__)
			else: # builtin modules
				graph.add_edge(hash(modulepath), hash(Python))
	return graph

def check_complexity(filepath):
	maintainability = 0
	size = 3 # minimum size
	with open(filepath) as source:
		halstead, cyclom, lloc, pcom = radon.metrics.mi_parameters(source.read(), count_multi=False)
		maintainability = radon.metrics.mi_compute(halstead, cyclom, lloc, pcom)
		size += math.sqrt(cyclom)

	hsb = secretary.value_to_HSB(maintainability)
	color = secretary.hsb_to_str(hsb)
	return size, color

def init(dirs):
	attributes = {}
	# Initialize a graph object
	attributes['graph'] = networkx.Graph()
	# Create the most basic node
	attributes['python'] = { 'type':'master', 'name':'Python',
							 'docstring':'Python builtin modules',
							 'filepath':'builtin', 'size':10,
							 'color':'#3776AB'} # color = dark blue
	attributes['finder'] = modulefinder.ModuleFinder(path=dirs)
	return attributes
