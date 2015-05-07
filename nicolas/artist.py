
import os
import json
import uuid
import shutil
import webbrowser
import pkg_resources
from networkx.readwrite import json_graph
from nicolas.parchment import pkginfo
from nicolas.atelier import draftsman

def draw(abspath, ignores):
	# path can be either relative or abs path
	dirs = list(pkginfo.get_directories(abspath))
	modules = pkginfo.get_modules(dirs)
	modules = pkginfo.filter_modules(modules, ignores)
	modules_paths = list(pkginfo.make_filepaths(modules))
	if pkginfo.is_package(abspath):
		dirs.append(os.path.dirname(abspath))

	graph = draftsman.sketch_blocks(modules_paths, dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	start_drawing(data)

def portrait(path):
	pass

def blame(path):
	pass

def trace(absfilepath):
	# create a list of dirs where to search for modules
	rootpath = os.path.dirname(absfilepath)
	ispkg = pkginfo.is_package(rootpath)
	while ispkg:
		rootpath = os.path.dirname(rootpath)
		ispkg = pkginfo.is_package(rootpath)
	dirs = list(pkginfo.get_directories(rootpath))
	# analyze module
	graph = draftsman.sketch_footprint(absfilepath, dirs)
	# write json formatted data
	data = json_graph.node_link_data(graph)
	 # create temp dir in cwd to avoid writing protected files
	start_drawing(data)
	pass

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
