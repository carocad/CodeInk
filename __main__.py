r"""
nikola draws your Python packages in his head.

Usage:
	nikola draw
	nikola portrait <file>
	nikola blame <file>
	nikola (-h | --help)
	nikola --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

__version__ = '0.0.5'

import docopt
import nikola

arguments = docopt.docopt(__doc__, version = __version__)

path = '.' # current directory
if arguments['draw']:
	nikola.draw(path)
elif arguments['portrait']:
	print(' Coming soon :)')
elif arguments['blame']:
	print(' Coming soon :)')
else:
	print(__doc__)
