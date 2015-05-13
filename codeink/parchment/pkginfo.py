import os
import pkgutil
import fnmatch
from itertools import filterfalse

def get_directories(path):
	for root, dirs, files in os.walk(path):
		if fnmatch.filter(files, '*.py'):
			yield root

def is_package(abspath):
	parent_path = os.path.dirname(abspath)
	for root, name, ispkg in pkgutil.iter_modules([parent_path]):
		if (ispkg and hasattr(root, 'path')
		and os.path.join(root.path, name) == abspath):
			return True
	return False

def get_modules(directories):
	for root, name, ispkg in pkgutil.iter_modules(directories):
		if hasattr(root, 'path') and not ispkg:
			yield os.path.join(root.path, name + '.py')

def filter_modules(modpaths, patterns):
	for pattern in patterns:
		# the pattern value is not frozen, thus a list has to be created
		# every time to execute the filtering process. Other option would
		# be to frozen the pattern value using functools.partial
		modpaths = list(
			filterfalse(lambda filepath: fnmatch.fnmatch(filepath, pattern),
						modpaths))
	return modpaths

def find_root_pkg(absfilepath):
	rootpath = os.path.dirname(absfilepath)
	ispkg = is_package(rootpath)
	while ispkg:
		rootpath = os.path.dirname(rootpath)
		ispkg = is_package(rootpath)
	return rootpath
