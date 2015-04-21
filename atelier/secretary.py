
import pyPeephole

def get_module_info(name, tree, path):
	_name = name
	_doc = pyPeephole.get_attr(tree, 'doc')
	_path = path
	return {'type':'module', 'name':_name, 'docstring':_doc, 'filepath':_path}

def get_function_info(func, path):
	_name = func.name
	_doc = pyPeephole.get_attr(func, 'doc')
	_str = pyPeephole.to_string(func)
	_path = path
	_lineno = func.lineno
	return {'type':'function', 'name':_name, 'docstring':_doc,
		   'definition':_str, 'filepath':_path, 'lineno':_lineno}

def get_class_info(classDef, path):
	_name = classDef.name
	_doc = pyPeephole.get_attr(classDef, 'doc')
	_str = pyPeephole.to_string(classDef)
	_path = path
	_lineno = classDef.lineno
	return {'type':'class', 'name':_name, 'docstring':_doc,
		   'definition':_str, 'filepath':_path, 'lineno':_lineno}

def get_import_info(importDef, alias, used_in):
	_name = alias.name
	_str = pyPeephole.to_string(importDef)
	_path = used_in
	_lineno = importDef.lineno
	return {'type':'import', 'name':_name, 'definition':_str,
			'used_in':_path, 'lineno':_lineno}

def get_importFrom_info(importFrom, used_in):
	_name = importFrom.module
	_str = pyPeephole.to_string(importFrom)
	_path = used_in
	_lineno = importFrom.lineno
	return {'type':'import', 'name':_name, 'definition':_str,
			'used_in':_path, 'lineno':_lineno}

def get_module_id(modules, name):
	for module in modules.keys():
		if name == module:
			return id(module)
