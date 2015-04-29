r"""
nikola draws your Python packages in his head.

Usage:
	daVinci draw
	daVinci find <definition>
	daVinci (-h | --help)
	daVinci --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

__version__ = '0.0.5'

import os
import docopt
import nikola

arguments = docopt.docopt(__doc__, version = __version__)

path = os.getcwd()
if arguments['draw']:
	nikola.draw(path)
elif arguments['find']:
	nikola.search(path, arguments['<definition>'])
else:
	print(__doc__)
