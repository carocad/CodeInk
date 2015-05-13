
import math
from radon import metrics
from codeink.atelier import secretary

def check_complexity(filepath):
	maintainability = 0
	size = 3 # minimum size
	with open(filepath) as source:
		halstead, cyclom, lloc, pcom = metrics.mi_parameters(source.read(),
															 count_multi=False)
		maintainability = metrics.mi_compute(halstead, cyclom, lloc, pcom)
		size += math.sqrt(cyclom)

	hsl = secretary.value_to_HSL(maintainability)
	color = secretary.hsl_to_str(hsl)
	return size, color

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
