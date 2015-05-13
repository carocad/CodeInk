
import os
import json
import uuid
import shutil
import webbrowser
import pkg_resources

from networkx.readwrite import json_graph

from codeink.parchment import pkginfo
from codeink.atelier import draftsman

def draw(abspath, ignores):
	# path can be either relative or abs path
	dirs = list(pkginfo.get_directories(abspath))
	modpaths = list(pkginfo.get_modules(dirs))
	modpaths = pkginfo.filter_modules(modpaths, ignores)
	if pkginfo.is_package(abspath):
		dirs.append(os.path.dirname(abspath))
	graph = draftsman.sketch_blocks(modpaths, dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	start_drawing(data)

def portrait(absfilepath):
	graph = draftsman.sketch_profile(absfilepath)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	start_drawing(data)

def blame(absfilepath, ignores):
	rootpath = pkginfo.find_root_pkg(absfilepath)
	dirs = list(pkginfo.get_directories(rootpath))
	modpaths = list(pkginfo.get_modules(dirs))
	modpaths = pkginfo.filter_modules(modpaths, ignores)
	graph = draftsman.sketch_accusation(absfilepath, modpaths, dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	start_drawing(data)

def trace(absfilepath):
	# create a list of dirs where to search for modules
	rootpath = pkginfo.find_root_pkg(absfilepath)
	dirs = list(pkginfo.get_directories(rootpath))
	# analyze module
	graph = draftsman.sketch_footprint(absfilepath, dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	start_drawing(data)
	## TODO: Change the trace module symbol

def start_drawing(data):
	canvas_dir = pkg_resources.resource_filename(__name__, 'canvas')
	tmp_dir = os.path.join(os.getcwd(), '.tmp' + str(uuid.uuid4()))
	html_tmp = os.path.join(tmp_dir, 'canvas.html')
	# create a temp directory and destroy it on exit
	try:
		shutil.copytree(src=canvas_dir, dst=tmp_dir, copy_function=shutil.copyfile)
		data_path = os.path.join(tmp_dir, 'data.json')
		with open(data_path, 'w') as jsonfile:
			json.dump(data, jsonfile)
		webbrowser.open_new_tab('file://%s' % html_tmp)
		print("\n\n ***** temporary files written to: ", tmp_dir, '\n\n')
	finally:
		input("Press <RETURN> to stop server\n")
		shutil.rmtree(path=tmp_dir)
		print("\nServer stoped, all temporary files deleted :) \n")
