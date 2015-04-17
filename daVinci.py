"""Module to find the Python files in a directory and parse them"""

import os
import collections
import networkx
import pyPeephole

def draw(path):
	mind = networkx.Graph()
	modules = parse_package(path)
	imports = fetch_imports(modules)
	merge_imports(imports)


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

def merge_imports(import_tuples):
	IMPORT_G = collections.namedtuple('import_group', 'name used_in')
	cache = {}
	for single in import_tuples:
		if single.name in cache:
			cache[single.name].used_in.append(single.path + ":L" + str(single.lineno))
		else:
			cache[single.name] = IMPORT_G._make([single.name,
												[single.path + ":L" + str(single.lineno)]])

def fetch_imports(modules):
	IMPORT_S = collections.namedtuple('import_single', 'name path lineno')
	for module in modules:
		for node in pyPeephole.get_imports(module.tree):
			for name in node.names:
				yield IMPORT_S._make([name.name, module.path, node.lineno])
		for node in pyPeephole.get_importsFrom(module.tree):
			yield IMPORT_S._make([node.module, module.path, node.lineno])

def parse_package(path):
	""" parse a Python package recursively and extract functions, classes
	 	and imports defined there"""
	MODULE = collections.namedtuple('module', 'name path tree')
	for path in find_pyFiles(path):
		name = os.path.basename(path)[:-3] #take the .py away
		tree = pyPeephole.parse(path)
		yield MODULE._make([name, path, tree])

def find_pyFiles(path):
	"find Python source code files contained in a directory"
	for path, dirs, files in os.walk(path):
		for filename in files:
			if filename.endswith('.py'):
				yield os.path.join(path, filename)
