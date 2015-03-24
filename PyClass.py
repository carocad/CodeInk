from pyclbr import Class, Function

class PyClass(object):
	#TODO add further methods that provide more information about each class
	def __init__(self, class_obj):
		self._module = class_obj.module
		self._name = class_obj.name
		self._parents = class_obj.super
		self._methods = class_obj.methods
		self._filename = class_obj.file
		self._lineno = class_obj.lineno

	def __repr__(self):
		# TODO: Why doesn't pyclbr parse some obj that are later showed as strings?
		parent_names = []
		for obj in self._parents:
			if isinstance(obj, str) and obj != "object":
				parent_names.append( "¿" + obj + "?")
			elif isinstance(obj, Class):
				parent_names.append("*" + obj.name + "*")
			else:
				parent_names.append("*" + obj + "*")
		parent_names = ", ".join(parent_names)
		result = ("class: {name} \n"
				  "\t inherits from: {parents} \n"
				  "\t defined at: {file}:L{line} \n"
				 ).format(name=self._name, parents=parent_names,
						  file=self._filename, line=self._lineno)

		for name, lineno in self._methods.items():
			if name != "__path__":
				descrp = ("{indent}method {name} defined at: L{line} \n"
						 ).format(name=name, line=lineno, indent="\t"*2)
				result += descrp
		return result
