from os import getcwd, walk
from PyFunction import PyFunction
from PyClass import PyClass
from pyclbr import readmodule_ex, Class, Function

class PkgHandler(object):
	#TODO add further methods that provide more information about the classes
	def __init__(self, path):
		self.path = path
		self.defs = {}

	def parse(self):
		modules = {}
		for path, dirs, files in walk(self.path):
			for filename in files:
				if filename.endswith('.py'):
					modules[filename[:-3]] = path

		for name, path in modules.items():
			try:
				if name in self.defs:
					continue
				classes = readmodule_ex(name, [path])
				for name, obj in classes.items():
					if isinstance(obj, Class):
						self.defs[name] = PyClass(obj)
					elif isinstance(obj, Function):
						self.defs[name] = PyFunction(obj)
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
						 "\t The passes value has an incorrect value \n"
						 "\t Traceback: {error} \n"
						).format(name=name, path=path, error=wrong_value)
				print(error)

	def classesToString(self):
		result = ""
		for definition in self.defs.values():
			if isinstance(definition, PyClass):
				result += repr(definition)
		return result

	def functionsToString(self):
		result = ""
		for definition in self.defs.values():
			if isinstance(definition, PyFunction):
				result += repr(definition)
		return result

