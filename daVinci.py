r"""
daVinci shows you easy diagrams of a Python packet structure.

Usage:
	daVinci draw
	daVinci sketch
	daVinci find
	daVinci (-h | --help)
	daVinci --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

import os
import docopt
import pyCrawler

def main():
	"""daVinci shows you easy diagrams of a Python packet structure."""
	arguments = docopt.docopt(__doc__, version = '0.0.1')

	#if arguments['draw']:
	path = os.getcwd()
	pyCrawler.parse_project(path)
	#else:
	#	print(__doc__)

#if __name__ == '__main__':
main()
