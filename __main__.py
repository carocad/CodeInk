r"""
daVinci shows you easy diagrams of a Python packet structure.

Usage:
	daVinci draw
	daVinci find <definition>
	daVinci (-h | --help)
	daVinci --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

__version__ = '0.0.1'

import os
import docopt
import daVinci

arguments = docopt.docopt(__doc__, version = __version__)

path = os.getcwd()
if arguments['draw']:
	daVinci.draw(path)
elif arguments['find']:
	daVinci.search(path, arguments['<definition>'])
else:
	print(__doc__)
