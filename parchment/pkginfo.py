
import os
import pkgutil

def get_directories(path):
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.py'):
				yield root
				break

def get_modules(directories):
	for root, name, ispkg in pkgutil.iter_modules(directories):
		if hasattr(root, 'path') and not ispkg:
			yield os.path.join(root.path, name + '.py')

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
