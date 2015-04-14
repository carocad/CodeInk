"""Module to find the Python files in a directory and parse them"""

import os
from PyPeepHole import PyPeepHole

def find_PyFiles(path):
	"find Python source code files contained in a directory"
	for path, dirs, files in os.walk(path):
		for filename in files:
			if filename.endswith('.py'):
				yield os.path.join(path, filename)

def parse_project(path):
	""" parse all Python source code files contained in a directory and extract
		their functions and classes declarations"""
	for path in find_PyFiles(path):
		tree = PyPeepHole.parse(path)
		for defs in PyPeepHole.get_classes(tree):
			print(PyPeepHole.to_string(defs))
		for defs in PyPeepHole.get_functions(tree):
			print(PyPeepHole.to_string(defs))
		for defs in PyPeepHole.get_imports(tree):
			print(PyPeepHole.to_string(defs))
