
import os
import modulefinder

import networkx

from nicolas.atelier import secretary
from nicolas.atelier import scientist

def sketch_blocks(modulepaths, pkg_dirs):
	attributes = init(pkg_dirs)
	graph = attributes['graph']
	Python = 'python'
	graph.add_node(Python, attributes[Python])
	for filepath in modulepaths:
		# bug - if the finder is not reinitialized, the previous modules.values()
		# 		are kept, thus been useless
		finder = modulefinder.ModuleFinder(path=pkg_dirs)
		print('processing:\t', filepath)
		# Calculate complexity and maintainability indexes
		size, color = scientist.check_complexity(filepath)
		# Insert current module info
		module_info = {'name':filepath, 'size':size, 'color':color}
		graph.add_node(filepath, module_info)
		# Find module imports
		finder.run_script(filepath)
		for edge in scientist.compute_edges(filepath, Python, finder.modules.values(),
											finder.badmodules.values()):
			graph.add_edge(*edge)
	return graph

def sketch_footprint(absfilepath, project_dirs):
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
		finder = modulefinder.ModuleFinder(path=pkg_dirs)
		# Calculate complexity and maintainability indexes
		size, color = scientist.check_complexity(modulepath)
		# Insert current module info
		module_info = {'name':modulepath, 'size':size, 'color':color}
		graph.add_node(modulepath, module_info)
		# Find module imports, ignore badmodules
		finder.run_script(modulepath)
		for edge in scientist.compute_edges(absfilepath, Python, finder.modules.values()):
			graph.add_edge(*edge)
		for module in finder.modules.values():
			if scientist.include_module(module):
				modules_to_check.append(module.__file__)
	return graph

def sketch_accusation(targetpath, modulepaths, project_dirs):
	graph = networkx.Graph()
	# Calculate complexity and maintainability
	size, color = scientist.check_complexity(targetpath)
	# Insert target module info
	target_info = {'name':targetpath, 'size':size, 'color':color}
	graph.add_node(targetpath, target_info)
	for modulepath in modulepaths:
		print('processing:\t', modulepath)
		finder = modulefinder.ModuleFinder(path=project_dirs)
		finder.run_script(modulepath)
		for module in finder.modules.values():
			if (scientist.include_module(module)
			and module.__file__ == targetpath):
				size, color = scientist.check_complexity(modulepath)
				module_info = {'name':modulepath, 'size':size, 'color':color}
				graph.add_node(modulepath, module_info)
				graph.add_edge(modulepath, targetpath)

	return graph

def init(dirs):
	attributes = {}
	# Initialize a graph object
	attributes['graph'] = networkx.Graph()
	# Create the most basic node
	attributes['python'] = { 'type':'master', 'name':'Python',
							 'docstring':'Python builtin modules',
							 'filepath':'builtin', 'size':10,
							 'color':'#3776AB'} # color = dark blue
	#attributes['finder'] = modulefinder.ModuleFinder(path=dirs)
	return attributes
