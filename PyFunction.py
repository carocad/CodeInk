from pyclbr import Function

class PyFunction(Function):

	def __init__(self, func_obj):
		super(PyFunction, self).__init__(func_obj.module, func_obj.name,
										 func_obj.file, func_obj.lineno)

	def __repr__(self):
		result = "function: " + self.name + \
				"\ndefined at: " #+ self.file + ":L" + self.lineno

		return result + "\n"