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
	python = object()
	mind.add_node(id(python), type='object', name='object',
					  doc=python.__doc__, path='builtin')
	#Make sure that all modules are on the graph
	for module_name in pkg_modules.keys():
		mind.add_node(id(module_name))

	# Add all the functions, classes and imports to the graph
	##  Also adds the details of each module
	for module_name, directory in pkg_modules.items():
		filepath = os.path.join(directory, module_name + '.py')
		current_tree = pyPeephole.parse(filepath)
		if current_tree is None: # in case of invalid syntax
			print('-------------INVALID SYNTAX ---------: ', filepath)
			continue
		# Insert current module
		mod_doc = pyPeephole.get_attr(current_tree, 'doc')
		mind.add_node(id(module_name), type='module', name=module_name,
					  doc=mod_doc, path=filepath)

		insert_functions(graph=mind, tree=current_tree,
						 parent_id=id(module_name), filepath=filepath)

		insert_classes(graph=mind, tree=current_tree,
					   parent_id=id(module_name), filepath=filepath)


		for node in pyPeephole.get_imports(current_tree):
			for alias in node.names:
				if alias.name in builtin_modules:
					#TODO differentiate between where the import is used to where it is located
					mind.add_node(id(alias), type='import', name=alias.name,
								  definition=pyPeephole.to_string(node),
								  path=filepath, lineno=node.lineno)
					mind.add_edge(id(python), id(alias))
					mind.add_edge(id(alias), id(module_name))
				elif alias.name in pkg_modules:
					#TODO differentiate between where the import is used to where it is located
					mind.add_node(id(alias), type='import', name=alias.name,
								  definition=pyPeephole.to_string(node),
								  path=filepath, lineno=node.lineno)
					mind.add_edge(id(alias), id(module_name))
					for key in pkg_modules.keys():
						if alias.name == key:
							mind.add_edge(id(alias), id(key))
				else:
					#TODO differentiate between where the import is used to where it is located
					mind.add_node(id(alias), type='import', name=alias.name,
								  definition=pyPeephole.to_string(node),
								  path=filepath, lineno=node.lineno)
					mind.add_edge(id(python), id(alias))
					mind.add_edge(id(alias), id(module_name))

		for node in pyPeephole.get_importsFrom(current_tree):
			#TODO differentiate between where the import is used to where it is located
			if node.module in builtin_modules:
				mind.add_node(id(node), type='import', name=node.module,
							  definition=pyPeephole.to_string(node),
							  path=filepath, lineno=node.lineno)
				mind.add_edge(id(python), id(node))
				mind.add_edge(id(node), id(module_name))
			#TODO differentiate between where the import is used to where it is located
			elif node.module in pkg_modules:
				mind.add_node(id(node), type='import', name=node.module,
							  definition=pyPeephole.to_string(node),
							  path=filepath, lineno=node.lineno)
				mind.add_edge(id(alias), id(module_name))
				for key in pkg_modules.keys():
					if alias.name == key:
						mind.add_edge(id(alias), id(key))
			#TODO differentiate between where the import is used to where it is located
			else:
				mind.add_node(id(node), type='import', name=node.module,
							  definition=pyPeephole.to_string(node),
							  path=filepath, lineno=node.lineno)
				mind.add_edge(id(python), id(node))
				mind.add_edge(id(node), id(module_name))

	print('----NODES------')
	for node_id in mind.nodes_iter():
		print(mind.node[node_id], '\n')
	print('----EDGES------')
	for from_id, to_id in mind.edges_iter():
		print('from ', from_id, 'to ', to_id, '\n')

def insert_functions(graph, tree, parent_id, filepath):
	for node in pyPeephole.get_functions(tree):
		func_doc = pyPeephole.get_attr(node, 'doc')
		graph.add_node(id(node), type='function', name=node.name,
					  doc=func_doc, definition=pyPeephole.to_string(node),
					  path=filepath, lineno=node.lineno)
		graph.add_edge(parent_id, id(node))

def insert_classes(graph, tree, parent_id, filepath):
	for node in pyPeephole.get_classes(tree):
		class_doc = pyPeephole.get_attr(node, 'doc')
		mind.add_node(id(node), type='class', name=node.name,
					  doc=class_doc, definition=pyPeephole.to_string(node),
					  path=filepath, lineno=node.lineno)
		mind.add_edge(parent_id, id(node))
		insert_functions(graph=mind, tree=node, parent_id=id(node), filepath=filepath)

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
