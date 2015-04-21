"""Module to find the Python files in a directory and parse them"""

from parchment import pkginfo
from atelier import draftsman

def draw(path):
	pkg_dirs = pkginfo.get_directories(path)
	pkg_modules = dict(pkginfo.get_modules(pkg_dirs))
	builtin_modules = dict(pkginfo.get_builtin_modules(ignore=pkg_modules))

	graph = draftsman.sketch_graph(pkg_modules, builtin_modules)
	print('----NODES------')
	for node_id in graph.nodes_iter():
		print(graph.node[node_id], '\n')
	print('----EDGES------')
	for from_id, to_id in graph.edges_iter():
		print('from ', from_id, 'to ', to_id, '\n')

def search(path, name):
	""" find the function or class definition with the specidfied name """
	for path in find_pyFiles(path):
		tree = pyPeephole.parse(path)
		match = pyPeephole.find(tree, name)
		if match:
			print(pyPeephole.to_string(match), " FILE: " + path)
			break
	else:
		print("\n I couldn't found the definition called {name}.\n".format(name=name),
			  "Check if the name is correct")
