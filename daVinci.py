"""Module to find the Python files in a directory and parse them"""

import os
import pyPeephole
import collections

def draw(path):
	modules = parse_package(path)

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

def find_pyFiles(path):
	"find Python source code files contained in a directory"
	for path, dirs, files in os.walk(path):
		for filename in files:
			if filename.endswith('.py'):
				yield os.path.join(path, filename)

def parse_package(path):
	""" parse all Python source code files contained in a directory and extract
		their functions and classes declarations"""
	MODULE = collections.namedtuple('module', 'name path tree')
	modules = set()
	for path in find_pyFiles(path):
		tree = pyPeephole.parse(path)
		name = os.path.basename(path)[:-3] #take the .py away
		modules.add(MODULE._make([name, path, tree]))
	return modules
