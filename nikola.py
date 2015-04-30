
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
	webbrowser.open_new('file://%s' % os.path.join(nikola_dir,'canvas/canvas.html'))

def portrait(path):
	pass

def blame(path):
	pass
