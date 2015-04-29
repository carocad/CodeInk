
import os
import json
import webbrowser
from networkx.readwrite import json_graph
from parchment import pkginfo
from atelier import draftsman

def draw(path):
	pkg_dirs = list(pkginfo.get_directories(path))
	project_modules = list(pkginfo.get_modules(pkg_dirs))

	graph = draftsman.sketch_blocks(project_modules, pkg_dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	# write json file
	nikola_dir = os.path.dirname(os.path.abspath(__file__))
	data_filepath = os.path.join(nikola_dir, 'canvas/data.json')
	json.dump(data, open(data_filepath, 'w'))
	print('\nJSON data written to:', data_filepath, '\n')
	# open URL in running web browser
	_load_url(os.path.join(nikola_dir,'canvas/canvas.html'))

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

def _load_url(path):
    webbrowser.open_new('file://%s' % (path))
