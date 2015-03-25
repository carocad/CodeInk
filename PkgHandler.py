from os import getcwd, walk
from PyObject import PyObject
from pyclbr import readmodule_ex, Class, Function

class PkgHandler(object):
	#TODO add further methods that provide more information about the classes
	def __init__(self, path):
		self.path = path
		self.objects = {}

	def parse(self):
		modules = {}
		for path, dirs, files in walk(self.path):
			for filename in files:
				if filename.endswith('.py'):
					modules[filename[:-3]] = path

		for name, path in modules.items():
			try:
				if name in self.objects:
					continue
				classes = readmodule_ex(name, [path])
				for name, obj in classes.items():
					if isinstance(obj, Class):
						self.objects[name] = PyObject(PyObject.CLASS, obj)
					elif isinstance(obj, Function):
						self.objects[name] = PyObject(PyObject.FUNCTION, obj)

			except ImportError as unknown_module:
				error = ("Unknown module {name} at {path} \n"
						 "\t Traceback: {error} \n"
						).format(name=name, path=path, error=unknown_module)
				print(error)
			except AttributeError as unknown_method:
				error = ("Unknown attribute for module {name} at {path} \n"
						 "\t Traceback: {error} \n"
						).format(name=name, path=path, error=unknown_method)
				print(error)
			except ValueError as wrong_value:
				error = ("Parsing error at module {name} in {path} \n"
						 "\t The passed value has an incorrect value \n"
						 "\t Traceback: {error} \n"
						).format(name=name, path=path, error=wrong_value)
				print(error)

	def classesToString(self):
		output = ""
		for definition in self.objects.values():
			if definition.getType() == PyObject.CLASS:
				output += repr(definition)
		return output

	def functionsToString(self):
		output = ""
		for definition in self.objects.values():
			if definition.getType() == PyObject.FUNCTION:
				output += repr(definition)
		return output

	def countFunctions(self):
		counter = 0
		for definition in self.objects.values():
			if definition.getType() == PyObject.FUNCTION:
				counter += 1
		return counter

	def countClasses(self):
		counter = 0
		for definition in self.objects.values():
			if definition.getType() == PyObject.CLASS:
				counter += 1
		return counter
