from pyclbr import Function

class PyFunction(object):

	def __init__(self, func_obj):
		self._module = func_obj.module
		self._name = func_obj.name
		self._filename = func_obj.name
		self._lineno = func_obj.lineno

	def __repr__(self):
		result = ("function: {name} \n"
				  "{indent}defined at: {fle}:L{line} \n"
				  "{indent} in module: {module} \n"
				  ).format(name=self._name, line=self._lineno,
						   fle=self._filename, indent="\t",
						   module = self._module)
		return result
