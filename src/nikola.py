
import os
import json
import webbrowser
import pkg_resources
from networkx.readwrite import json_graph
from .parchment import pkginfo
from .atelier import draftsman

def draw(path):
	pkg_dirs = list(pkginfo.get_directories(path))
	project_modules = list(pkginfo.get_modules(pkg_dirs))

	graph = draftsman.sketch_blocks(project_modules, pkg_dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	canvas_dir = pkg_resources.resource_filename(__name__, 'canvas') # relative path
	canvas_dir = os.path.abspath(canvas_dir) # absolute path
	data_file = os.path.join(canvas_dir, 'data.json')
	html_file = os.path.join(canvas_dir, 'canvas.html')
	# write json file
	with open(data_file, 'w') as jsondata:
		json.dump(data, jsondata)
	# open URL in running web browser
	webbrowser.open_new_tab('file://%s' % html_file)

def portrait(path):
	pass

def blame(path):
	pass
