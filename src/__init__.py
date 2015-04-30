r"""
nicolas draws your Python modules into a graph.

Usage:
	nicolas draw <directory>
	nicolas portrait <file>
	nicolas blame <file>
	nicolas (-h | --help)
	nicolas --version

Options:
	-h --help Show this screen.
	--version Show version.

"""

__version__ = '0.0.4'

def main(args=None):

	import docopt
	from src import nicolas

	arguments = docopt.docopt(__doc__, version = __version__)
	if arguments['draw']:
		path = arguments['<directory>']
		nicolas.draw(path)
	elif arguments['portrait']:
		print(' Coming soon :)')
	elif arguments['blame']:
		print(' Coming soon :)')
	else:
		print(__doc__)

if __name__ == '__main__':
	main()
