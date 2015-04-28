
import networkx
import math
import radon.metrics
import pyPeephole
from . import secretary

def sketch_blocks(project_modules, project_pkgs):
	# Initialize a graph object
	graph = networkx.Graph()
	# Create the most basic node
	Python = 'Python'
	graph.add_node(Python, type='master', name=Python,
				  docstring='Python builtin modules', filepath='builtin',
				  size=10, color='#004C00')

	# First parse init files to resolve hidden imports
	## It is assumed that a package will not import another package
	hidden_imports = {}
	for package, init_file in project_pkgs.items():
		ast_tree = pyPeephole.parse(init_file)
		if ast_tree is None: # in case of invalid syntax
			continue
		for importDef in pyPeephole.get_imports(ast_tree):
			names = secretary.resolve_import(importDef.names)
			modules = hidden_imports.setdefault(package, set())
			prj_names = set(secretary.filter_project_modules(names, project_modules,
															 default=Python))
			modules |= prj_names
		for importFrom in pyPeephole.get_importsFrom(ast_tree):
			names = secretary.resolve_from_import(importFrom, project_modules)
			modules = hidden_imports.setdefault(package, set())
			prj_names = set(secretary.filter_project_modules(names, project_modules,
															 default=Python))
			modules |= prj_names

	#for name, value in hidden_imports.items():
		#print(name, '--->', value)

	# Second parse each module and resolve its imports
	for module, filepath in project_modules.items():
		ast_tree = pyPeephole.parse(filepath)
		if ast_tree is None: # in case of invalid syntax
			continue
		# Insert current module info
		module_info = secretary.get_module_info(module, ast_tree, filepath)
		graph.add_node(module, module_info)
		# Calculate complexity and maintainability indexes
		size, color = check_complexity(ast_tree, filepath)
		graph.add_node(module, size=size, color=color)
		# Insert imports info
		imports = set()
		for importDef in pyPeephole.get_imports(ast_tree):
			names = secretary.resolve_import(importDef.names)
			for name in names:
				if name in hidden_imports: # package imported
					imports |= hidden_imports[name]
				elif name in project_modules:
					imports.add(name)
				else: # builtin import
					imports.add(Python)

		# Insert from Foo import bar
		for importFrom in pyPeephole.get_importsFrom(ast_tree):
			names = secretary.resolve_from_import(importFrom, project_modules)
			prj_names = set(secretary.filter_project_modules(names, project_modules,
															 default=Python))
			imports |= prj_names
		## Add a link from each module to the current one
		#print(module, imports)
		graph.add_star([module] + list(imports))
		graph.add_node(module, impno=len(imports))
	return graph

def check_complexity(ast_tree, filepath):
	maintainability = 0
	size = 3 # minimum size
	with open(filepath) as source:
		halstead, cyclom, lloc, pcom = radon.metrics.mi_parameters(source.read(), count_multi=False)
		maintainability = radon.metrics.mi_compute(halstead, cyclom, lloc, pcom)
		size += math.sqrt(cyclom)

	rgb = secretary.value_to_RGB(maintainability)
	color = secretary.rgb_to_hex(rgb)
	return size, color
