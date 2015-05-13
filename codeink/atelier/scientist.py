
import math
from radon import metrics
from codeink.atelier import secretary
from itertools import filterfalse

def check_complexity(filepath):
	maintainability = 0
	size = 3 # minimum size
	with open(filepath) as source:
		cyclom, maintainability = calculate_complexity(source.read())
		size += math.sqrt(cyclom)

	hsl = secretary.value_to_HSL(maintainability)
	color = secretary.hsl_to_str(hsl)
	return size, color

def check_snippet_complexity(strcode, initsize=3):
	size = initsize # minimum size
	cyclom, maintainability = calculate_complexity(strcode)
	size += math.sqrt(cyclom)

	hsl = secretary.value_to_HSL(maintainability)
	color = secretary.hsl_to_str(hsl)
	return size, color

def calculate_complexity(sourcecode):
	halstead, cyclom, lloc, pcom = metrics.mi_parameters(sourcecode,
														 count_multi=False)
	maintainability = metrics.mi_compute(halstead, cyclom, lloc, pcom)
	return cyclom, maintainability

def compute_edges(filepath, base, found_imports, missing_imports=None):
	for module in found_imports:
		if include_module(module):
			yield (filepath, module.__file__)
		else: # builtin modules not found
			yield (filepath, base)
	if missing_imports:
		yield (filepath, base)

def include_module(module):
	return (module.__file__ is not None
			and not module.__file__.endswith('__init__.py')
			#and filepath != module.__file__
			and module.__name__ != '__main__')

def filtertype(objtype, iterable, filterfalse=False):
	filterfn = filter if not filterfalse else filterfalse
	return filterfn(lambda element: isinstance(element, objtype), iterable)
