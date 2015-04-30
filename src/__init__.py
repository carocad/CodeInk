r"""
nikola draws your Python modules into a graph.

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

__version__ = '0.0.3'

def main(args=None):

	import docopt
	from src import nikola

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

if __name__ == '__main__':
	main()
