
import os

from codeink.parchment import peephole

def get_module_info(tree, absfilepath):
	_name = os.path.basename(absfilepath)[:-3] # strip the .py from filepath
	_doc = peephole.get_attr(tree, 'doc')
	_path = absfilepath
	return {'type':'module', 'name':_name, 'docstring':_doc, 'filepath':_path}

def get_function_info(func, path):
	_name = func.name
	_doc = peephole.get_attr(func, 'doc')
	_str = peephole.to_string(func)
	_path = path
	_lineno = func.lineno
	return {'type':'function', 'name':_name, 'docstring':_doc,
		   'definition':_str, 'filepath':_path, 'lineno':_lineno}

def get_class_info(classDef, path):
	_name = classDef.name
	_doc = peephole.get_attr(classDef, 'doc')
	_str = peephole.to_string(classDef)
	_path = path
	_lineno = classDef.lineno
	return {'type':'class', 'name':_name, 'docstring':_doc,
		   'definition':_str, 'filepath':_path, 'lineno':_lineno}

def value_to_HSL(value):
	# max(value) = 100
	hue = value * 1.2 # 1.2 = green, 0 = red
	saturation = 90
	lightness = 40
	return (hue, saturation, lightness)

def hsl_to_str(HSL):
    return 'hsl({h}, {s}%, {l}%)'.format(h=HSL[0], s=HSL[1], l=HSL[2])

def make_scoped_name(*scopes):
	return '.'.join(scopes)
