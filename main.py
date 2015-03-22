"""
daVinci generates html files with drawings of your Python project source code.

Usage:
	daVinci draw
	daVinci -h | --help
	daVinci --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

from os import getcwdu
from docopt import docopt
from pyclbr import readmodule_ex


def _main():
	'''daVinci generates html files with drawings of your Python project source code.'''
  	arguments = docopt(__doc__, version = '0.0.1')

  	if arguments['draw']:
		print('test')
	else:
		print(__doc__)

if __name__ == '__main__':
	_main()
