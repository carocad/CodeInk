
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

def resolve_from_import(importFrom, project_modules):
	if importFrom.module is not None:
		## from .pkg.module import function/class
		return set([resolve_name(importFrom.module)])
	else:
		## from .pkg import module1, module2
		# from . import module
		return set(resolve_import(importFrom.names))

def resolve_import(names):
	for alias in names:
		yield resolve_name(alias.name)

def resolve_name(name):
	if '.' in name: ## import foo.bar
		chain = name.split('.')
		return chain[-1] ### bar
	else: # import Foo
		return name

def filter_project_modules(names, project_modules, default):
	for name in names:
		if name in project_modules:
			yield name
		else:
			yield default

def value_to_RGB(value):
	# max(value) = 100
	R = (255 * (100 - value) )/ 100
	G = (255 * value) / 100
	B = 0
	return (R, G, B)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
