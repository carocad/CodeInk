"""Module to find the Python files in a directory and parse them"""

import os
import collections
import networkx
import pyPeephole
import pkgutil

def draw(path):
	mind = networkx.Graph()
	#TODO create a graph base on the imports, functions and classes
	pkg_dirs = {path for path, dirs, files in os.walk(path)} # set comprehension
	pkg_modules = {name:path.path for path, name, ispkg in pkgutil.iter_modules(pkg_dirs)
				   					if hasattr(path, 'path')
				   					and not ispkg} #dict comprehension
	builtin_modules = {name:path.path for path, name, ispkg in pkgutil.iter_modules()
					  					if hasattr(path, 'path')
					   					and path.path not in pkg_dirs} #dict comprehension

	#MODULE = collections.namedtuple('modules', 'name path doc definitions')
	#IMPORT = collections.namedtuple('imports', 'module path lineno definition')
	#CLASS = collections.namedtuple('classes', 'module name path lineno doc definition')
	#FUNCTION = collections.namedtuple('functions', 'module name path lineno doc definition')
	for module_name, directory in pkg_modules.items():
		filepath = os.path.join(directory, module_name + '.py')
		tree = pyPeephole.parse(filepath)
		if not tree: # in case of invalid syntax
			print('module avoided')
			continue
		mod_doc = pyPeephole.get_attr(tree, 'doc')
		mind.add_node(id(module_name), type='module', name=module_name,
					  doc=mod_doc, path=filepath)
		for node in pyPeephole.get_functions(tree):
			func_doc = pyPeephole.get_attr(node, 'doc')
			mind.add_node(id(node.name), type='function', name=node.name,
						  doc=func_doc, definition=pyPeephole.to_string(node),
						  path=filepath, lineno=node.lineno)
			mind.add_edge(id(module_name), id(node.name))
		for node in pyPeephole.get_classes(tree):
			class_doc = pyPeephole.get_attr(node, 'doc')
			mind.add_node(id(node.name), type='class', name=node.name,
						  doc=class_doc, definition=pyPeephole.to_string(node),
						  path=filepath, lineno=node.lineno)
			mind.add_edge(id(module_name), id(node.name))
			#TODO add the class methods to the graph

#			elif isinstance(node, ast.ClassDef):
#			elif isinstance(node, ast.Import):
#			elif isinstance(node, ast.ImportFrom):
	for node_id in mind.nodes_iter():
		print(mind.node[node_id], '\n')
	print(mind.edges())

def search(path, name):
	""" find the function or class definition with the specidfied name """
	for path in find_pyFiles(path):
		tree = pyPeephole.parse(path)
		match = pyPeephole.find(tree, name)
		if match:
			print(pyPeephole.to_string(match), " FILE: " + path)
			break
	else:
		print("\n I couldn't found the definition called {name}.\n".format(name=name),
			  "Check if the name is correct")
