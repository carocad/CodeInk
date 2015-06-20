""" functions used to execute the users request passed trough the
command line.
"""

import os
import json
import uuid
import shutil
import webbrowser
import pkg_resources

from networkx.readwrite import json_graph

from codeink.parchment import pkginfo
from codeink.atelier import draftsman

def draw(absdirpath, excluding):
    """open a browsers tab to display a graph of all the modules under `absdirpath`, excluding those
    specified by `excluding`. 

    Args:
        absdirpath (str): absolute directory path used as the root for populating
          the modules list.
        excluding (List[str]): list of Unix shell-style wildcards strings used to 
          exclude modules from being analyzed.
    """
    dirs = list(pkginfo.get_directories(absdirpath))
    modpaths = list(pkginfo.get_modules(dirs))
    modpaths = pkginfo.filter_modules(modpaths, excluding)
    if pkginfo.is_package(absdirpath):
        dirs.append(os.path.dirname(absdirpath))
    graph = draftsman.sketch_blocks(modpaths, dirs)
    # write json formatted data
    data = json_graph.node_link_data(graph)
     # create temp dir in cwd to avoid writing protected files
    start_drawing(data)

def portrait(absfilepath):
    """open a browsers tab to display a graph of all the functions and classes
    defined at `absfilepath`.

    Args:
        absfilepath (str): absolute filepath of the module to portrait.
    """
    graph = draftsman.sketch_profile(absfilepath)
    # write json formatted data
    data = json_graph.node_link_data(graph)
     # create temp dir in cwd to avoid writing protected files
    start_drawing(data)

def blame(absfilepath, excluding):
    """open a browsers tab to display a graph of all the modules that import the
    module at `absfilepath`, excluding those specified by `excluding`

    Args:
        absfilepath (str): absolute filepath of the module to check for.
        excluding (List[str]): list of Unix shell-style wildcards strings used to 
          exclude modules from being analyzed.
    """
    rootpath = pkginfo.find_root_pkg(absfilepath)
    dirs = list(pkginfo.get_directories(rootpath))
    modpaths = list(pkginfo.get_modules(dirs))
    modpaths = pkginfo.filter_modules(modpaths, excluding)
    graph = draftsman.sketch_accusation(absfilepath, modpaths, dirs)
    # write json formatted data
    data = json_graph.node_link_data(graph)
     # create temp dir in cwd to avoid writing protected files
    start_drawing(data)

def trace(absfilepath):
    """open a browsers tab to display the graph of all the modules imported by the
    module at `absfilepath` either directly or indirectly.

    Args:
        absfilepath (str): absolute filepath of the module to analyze.
    """
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
    """creates a temporary directory to where the HTML, Javascript and CSS files
    are copied for later rendering in a webbrowser.
    This function opens a new tab in a webbroser using the copied files and
    waits for input at the command line to delete all the files created.

    Args:
        data (Dict[str, Dict[str, Any]]): data in node-link format suitable for JSON serialization
          and use in Javascript documents.
    """
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
