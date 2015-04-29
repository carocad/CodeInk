"""Module to find the Python files in a directory and parse them"""

import os
import json
from networkx.readwrite import json_graph
from parchment import pkginfo
from atelier import draftsman

def draw(path):
	pkg_dirs = set(pkginfo.get_directories(path))
	project_modules = dict(pkginfo.get_modules(pkg_dirs))
	project_pkgs = dict(pkginfo.get_packages(pkg_dirs))

	graph = draftsman.sketch_blocks(project_modules, project_pkgs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	# write json file
	daVinci_dir = os.path.dirname(os.path.abspath(__file__))
	data_filepath = os.path.join(daVinci_dir, 'canvas/data.json')
	json.dump(data, open(data_filepath, 'w'))
	print('\nJSON data written to:', data_filepath, '\n')
	#print('----NODES------')
	#for node_id in graph.nodes_iter():
		#print(graph.node[node_id], '\n')
	#print('----EDGES------')
	#for from_id, to_id in graph.edges_iter():
		#print('from ', from_id, 'to ', to_id, '\n')

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
