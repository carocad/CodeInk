from pyclbr import Function

class PyFunction(object):

	def __init__(self, func_obj):
		self._module = func_obj.module
		self._name = func_obj.name
		self._filename = func_obj.name
		self._lineno = func_obj.lineno

	def __repr__(self):
		result = ("function: {name} \n"
				  "\t defined at: {fle}:L{line} \n"
				  "\t in module: {module} \n"
				  ).format(name=self._name, line=self._lineno,
						   fle=self._filename, indent="\t",
						   module = self._module)
		return result

	def __hash__(self):
		return hash(self._name + self._filename) + self._lineno

	def __eq__(self, other):
		if self._name != other._name:
			return false
		elif self._filename != other._filename:
			return false
		elif self._lineno != other._lineno:
			return false
		else:
			return true

	def isObjectSubclass(self):
		return true
