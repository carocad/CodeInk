import os
import pkgutil
import fnmatch

def get_directories(dirpath, extension='.py'):
	for root, dirs, files in os.walk(dirpath):
		for file in files:
			if fnmatch.fnmatch(file, '*' + extension):
				yield root
				break

def is_package(absdirpath):
	parent_dir = os.path.dirname(absdirpath)
	pkg_name = os.path.basename(absdirpath)
	for root, name, ispkg in pkgutil.iter_modules([parent_dir]):
		if ispkg and name == pkg_name:
			return True
	return False

def get_modules(directories):
	for root, name, ispkg in pkgutil.iter_modules(directories):
		if hasattr(root, 'path') and not ispkg:
			yield os.path.join(root.path, name + '.py')

def filter_modules(modpaths, patterns):
	for pattern in patterns:
		modpaths = [ filepath for filepath in modpaths
			  		 if not fnmatch.fnmatch(filepath, pattern) ]
	return modpaths

def find_root_pkg(absfilepath):
	rootpath = os.path.dirname(absfilepath)
	ispkg = is_package(rootpath)
	while ispkg:
		rootpath = os.path.dirname(rootpath)
		ispkg = is_package(rootpath)
	return rootpath
