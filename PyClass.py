from pyclbr import Class, Function

class PyClass():

	def __init__(self, class_obj):
		self.module = class_obj.module
		self.name = class_obj.name
		self.parents = class_obj.super
		self.methods = class_obj.methods
		self.filename = class_obj.file
		self.lineno = class_obj.lineno

	def __repr__(self):
		result = ("class: {0}"
				  "\n\tinherits from: {1}"
				  "\n\tdefined at: {2}:L{3}").format(self.name, 'test',
													 self.filename, self.lineno)

		for name, lineno in self.methods.items():
			if name != "__path__":
				descrp = "\n\t\tmethod {} defined at: L{}".format(name, lineno)
				result += descrp

		return result + "\n"
