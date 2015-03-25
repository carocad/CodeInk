"""
daVinci shows you easy diagrams of a Python packet structure.

Usage:
	daVinci draw
	daVinci sketch
	daVinci write
	daVinci -h | --help
	daVinci --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

from os import getcwd
from docopt import docopt
from PkgHandler import PkgHandler

def _main():
	"daVinci shows you easy diagrams of a Python packet structure."
	arguments = docopt(__doc__, version = '0.0.1')

	if arguments['draw']:
		cwd = getcwd()
		pkg = PkgHandler(cwd)
		pkg.parse()

		print(pkg.classesToString())
		print(pkg.functionsToString())
	else:
		print(__doc__)

if __name__ == '__main__':
	_main()
