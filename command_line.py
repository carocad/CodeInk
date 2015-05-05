r"""
nicolas draws your Python modules into a graph.

Usage:
	nicolas draw <directory> [--ignore <pattern>...]
	nicolas portrait <file>
	nicolas blame <file>
	nicolas trace <file>
	nicolas (-h | --help)
	nicolas --version

Options:
	-h --help	Show this screen.
	--version	Show version.
	--ignore	Pattern to ignore.

"""

# TODO put an ignore flag in the usage to ignore files and/or directories
# 	   that should not be scaned for dependencies and/or complexity

import os
import docopt
from src import nicolas
from src import __version__

def main(args=None):

	arguments = docopt.docopt(__doc__, version = __version__)
	if arguments['draw']:
		path = os.path.abspath(arguments['<directory>'])
		ignore = arguments['<pattern>']
		nicolas.draw(path, ignore)
	elif arguments['portrait']:
		print(' Coming soon :)')
	elif arguments['blame']:
		print(' Coming soon :)')
	else:
		print(__doc__)

if __name__ == '__main__':
	main()
