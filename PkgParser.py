from os import getcwd, walk
from PyFunction import PyFunction
from PyClass import PyClass
from pyclbr import readmodule_ex, Class, Function

class PkgHandler():

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
			except ImportError as error:
				print(error)

	def defsToString(self):
		result = ""
		for definition in self.defs.values():
			result += repr(definition)

		return result
