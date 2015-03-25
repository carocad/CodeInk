from pyclbr import Class

class PyObject(object):
	#TODO add further methods that provide more information about each class
	CLASS = 0
	FUNCTION = 1
	TYPE_OBJECT = "object"

	def __init__(self, tag, obj):
		self._type = tag
		self._module = obj.module
		self._name = obj.name
		self._filename = obj.file
		self._lineno = obj.lineno

		if tag == self.CLASS:
			self._parents = obj.super
			# Transform the parents into PyObject
			for index, parent in enumerate(self._parents):
				if isinstance(parent, str):
					continue
				else:
					self._parents[index] = PyObject(self.CLASS, parent)
			self._methods = obj.methods
		elif tag == self.FUNCTION:
			self._parents = [self.TYPE_OBJECT]
			self._methods = []
		else:
			raise ValueError("Unknown tag passed: " + tag)

		if self.isObjectSubclass():
			self._parents = [self.TYPE_OBJECT]

	def __repr__(self):
		# TODO: Why doesn't pyclbr parse some obj that are later showed as strings?
		parent_names = []
		output = ""
		if self._type == self.CLASS:
			for obj in self._parents:
				if isinstance(obj, str) and obj != "object":
					parent_names.append( "¿" + obj + "?")
				elif isinstance(obj, Class):
					parent_names.append("*" + obj.name + "*")
				else:
					parent_names.append("*" + obj + "*")
			parent_names = ", ".join(parent_names)
			output = ("class: {name} \n"
					  "\t inherits from: {parents} \n"
					  "\t defined at: {filename}:L{line} \n"
				 	).format(name=self._name, parents=parent_names,
						  	 filename=self._filename, line=self._lineno)

			for name, lineno in self._methods.items():
				if name != "__path__":
					descrp = ("\t\t method {name} defined at: L{line} \n"
							 ).format(name=name, line=lineno)
					output += descrp
		else:
			output = ("function: {name} \n"
					  "\t defined at: {fle}:L{line} \n"
					  "\t in module: {module} \n"
					 ).format(name=self._name, line=self._lineno,
							  fle=self._filename, indent="\t",
							  module = self._module)
		return output

	def __hash__(self):
		return hash(self._name + self._filename) + self._lineno

	def __eq__(self, other):
		if not isinstance(other, PyObject):
			return False
		if self._name != other._name:
			return False
		elif self._filename != other._filename:
			return False
		elif self._lineno != other._lineno:
			return False
		else:
			return True

	def countMethods(self):
		return len(self._methods)

	def isObjectSubclass(self):
		if len(self._parents) == 0:
			return True
		elif len(self._parents) > 1: # object can only be inherited once
			return False
		elif self._parents[0] == self.TYPE_OBJECT or self._parents[0] == "":
			return True

	def hasMultipleParents(self):
		if len(self._parents) > 1:
			return True
		else:
			return False

	def getName(self):
		return self._name

	def getModuleName(self):
		return self._module

	def getFilename(self):
		return self._filename

	def getType(self):
		return self._type
