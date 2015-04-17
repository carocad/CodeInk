"""Module to find the Python files in a directory and parse them"""

import os
import pyPeephole

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
		tree = pyPeephole.parse(path)
		for defs in pyPeephole.get_classes(tree):
			print(pyPeephole.to_string(defs))
		for defs in pyPeephole.get_functions(tree):
			print(pyPeephole.to_string(defs))
		for defs in pyPeephole.get_imports(tree):
			print(pyPeephole.to_string(defs))
