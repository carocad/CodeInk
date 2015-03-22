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

from os import getcwdu, walk, path
from docopt import docopt
from pyclbr import readmodule_ex, Class, Function
from operator import itemgetter


def _main():
	'''daVinci generates html files with drawings of your Python project source code.'''
  	arguments = docopt(__doc__, version = '0.0.1')

  	if arguments['draw']:
		modules = {}
		cwd = getcwdu()
		for path, dirs, files in walk(cwd):
			for file in files:
				if file.endswith('.py'):
					modules[file[:-3]] = path

		definitions = []
		for name, path in modules.items():
			try:
				dict = readmodule_ex(name, [path])
			except ImportError:
				print "Error: failed to find module: ", name, " in ", path
			classes = dict.values()
			if classes:
				definitions.extend(classes)

		for obj in definitions:
			if isinstance(obj, Class):
				print "class", obj.name, obj.super, obj.lineno
				methods = sorted(obj.methods.iteritems(), key=itemgetter(1))
				for name, lineno in methods:
					if name != "__path__":
						print "  def", name, lineno
			elif isinstance(obj, Function):
				print "def", obj.name, obj.lineno

	else:
		print(__doc__)

if __name__ == '__main__':
	_main()
