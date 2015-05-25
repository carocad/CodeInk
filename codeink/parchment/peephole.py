""" parses a python module and find information about classes, functions
	and import statements there.

	* Copyright (c) 2015 Camilo Roca, carocad@unal.edu.co
"""

import ast
import astunparse
import copy
import functools
import textwrap

def parse(path):
	"parse a file at path and returns an AST tree structure"
	tree = None
	try:
		source_code = open(path)
		tree = ast.parse(source_code.read(), path)
		return tree
	except SyntaxError as e: ## parsing a python code from a different Python version
		print('Invalid syntax: {text} in {filename}:L{lineno}'.format(text=e.text,
															 filename=e.filename,
															 lineno=e.lineno))
	finally:
		source_code.close()
	return tree

def get_classes(node):
	"get the class definitions inside node"
	return filter( (lambda child: isinstance(child, ast.ClassDef)),  node.body)

def get_functions(node):
	"get the function definitions inside node"
	return filter( (lambda child: isinstance(child, ast.FunctionDef)),  node.body)

def get_imports(node):
	"get the import definitions inside node"
	return filter( (lambda child: isinstance(child, ast.Import)), node.body)

def get_importsFrom(node):
	"get the import from definitions inside node"
	return filter( (lambda child: isinstance(child, ast.ImportFrom)), node.body)

def get_attr(node, name):
	"get the attribute of node or None if the attribute doesn't exist"
	if name == 'doc':
		return str(ast.get_docstring(node, clean=True))
	if hasattr(node, name):
		return getattr(node, name)
	return None

@functools.lru_cache(maxsize=32)
def find(node, name):
	""" find a child (recursively) inside node with the specified name."""
	for child in ast.walk(node):
		if (isinstance(child, ast.ClassDef) or isinstance(child, ast.FunctionDef)) \
			and child.name == name:
				return child
	return None

def to_string(node, doc=False, lineno=False):
	""" transform an ast node of type FunctionDef, ClassDef or Import
		into a string with basic information """
	if isinstance(node, ast.FunctionDef):
		return function_to_string(node, doc, lineno)
	elif isinstance(node, ast.ClassDef):
		return class_to_string(node, doc, lineno)
	elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
		return import_to_string(node, lineno)
	return None

def function_to_string(FunctionDef, doc=False, lineno=False):
	""" transform an ast node of type FunctionDef into a string with basic information """
	tmp_def = copy.copy(FunctionDef)
	tmp_def.body = []

	funct_str = astunparse.unparse(tmp_def)
	if doc:
		funct_str += '\"\"\"' + get_attr(FunctionDef, 'doc') + '\"\"\"\n'
	if lineno:
		funct_str += "#lineno: " + str(FunctionDef.lineno)
	return funct_str

def class_to_string(ClassDef, doc=False, lineno=False):
	""" transform an ast node of type ClassDef into a string with basic information """
	tmp_def = copy.copy(ClassDef)
	tmp_def.body = []
	methods = [function_to_string(func, doc, lineno) for func in get_functions(ClassDef)]
	methods_str = "".join(methods)

	class_str = astunparse.unparse(tmp_def)
	if doc:
		class_str += '\"\"\"' + get_attr(ClassDef, 'doc') + '\"\"\"\n'
	if lineno:
		class_str += "#lineno: " + str(ClassDef.lineno)
	class_str += textwrap.indent(methods_str, '\t')
	return class_str

def import_to_string(importDef, lineno=False):
	""" transform an ast node of type ClassDef into a string """
	import_str = astunparse.unparse(importDef)
	if lineno:
		import_str += '#lineno: ' + str(importDef.lineno)
	return import_str
