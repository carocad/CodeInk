
import os
import pkgutil
import fnmatch

def get_directories(path):
	for root, dirs, files in os.walk(path):
		if fnmatch.filter(files, '*.py'):
			yield root

def is_package(abspath):
	parent_path = os.path.dirname(abspath)
	for root, name, ispkg in pkgutil.iter_modules([parent_path]):
		if ispkg and hasattr(root, 'path') \
			and os.path.join(root.path, name) == abspath:
			return True
	return False

def get_modules(directories):
	for root, name, ispkg in pkgutil.iter_modules(directories):
		if hasattr(root, 'path') and not ispkg:
			yield (root.path, name + '.py')

def filter_modules(modules, patterns):
	for pattern in patterns:
		modules = filter( lambda module: fnmatch.fnmatch(module[1], pattern),
						  modules)
	return modules

def make_filepaths(modules):
	for root, filename in modules:
		yield  os.path.join(root, filename)

def get_packages(directories):
	for root, name, ispkg in pkgutil.iter_modules(directories):
		if hasattr(root, 'path') and ispkg:
			yield os.path.join(root.path, name, '__init__.py')

def get_builtin_modules(ignore):
	for root, name, ispkg in pkgutil.iter_modules():
		if hasattr(root, 'path') and name not in ignore and not ispkg:
			yield name, os.path.join(root.path, name + '.py')

def get_builtin_packages(ignore):
	for root, name, ispkg in pkgutil.iter_modules():
		if hasattr(root, 'path') and name not in ignore and ispkg:
			yield name, os.path.join(root.path, name, '__init__.py')
