
import os
import json
import tempfile
import shutil
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
	start_drawing(data)

def portrait(path):
	pass

def blame(path):
	pass

def start_drawing(data):
	canvas_dir = pkg_resources.resource_filename(__name__, 'canvas')
	html_path = os.path.join(canvas_dir, 'canvas.html')
	css_path = os.path.join(canvas_dir, 'cubism.css')
	js_path = os.path.join(canvas_dir, 'hand.js')
	# create a temp directory and destroy it on exit
	with tempfile.TemporaryDirectory(prefix='.tmp', dir=os.getcwd()) as tmp_dir:
		html_tmp = os.path.join(tmp_dir, 'canvas.html')
		css_tmp = os.path.join(tmp_dir, 'cubism.css')
		js_tmp = os.path.join(tmp_dir, 'hand.js')
		shutil.copyfile(html_path, html_tmp)
		shutil.copyfile(css_path, css_tmp)
		shutil.copyfile(js_path, js_tmp)
		# write json file
		data_path = os.path.join(tmp_dir, 'data.json')
		with open(data_path, 'w') as jsonfile:
			json.dump(data, jsonfile)
		# open URL in running web browser
		webbrowser.open_new_tab('file://%s' % html_tmp)
		input("Press <RETURN> to stop server\n")
		print("Server stoped, all temporary files deleted")
