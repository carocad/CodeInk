
from setuptools import setup, find_packages
import codeInk

setup(
    name = 'codeInk',
    version = nicolas.__version__,
    description = 'codeInk draws your Python source code into beautiful graph structures',
    long_description = open('README.md').read(),
    author = nicolas.__author__,
    author_email = nicolas.__author_email__,
    license = nicolas.__license__,
    keywords = ['graph', 'module', 'complexity', 'maintainability', 'import'],
    url = nicolas.__URL__,
    packages = find_packages(),
	py_modules = ['codeink_cli'],
	package_data = { 'codeink.canvas': ['hand.js',
							 			'canvas.html',
							 			'cubism.css'] },
    install_requires = ['docopt>=0.6.2',
						'networkx>=1.9.1',
						'radon>=1.2' ],
    classifiers = ['Development Status :: 3 - Alpha',
				 	'Topic :: Utilities',
				 	'Programming Language :: Python :: 3'],
    entry_points = {'console_scripts': [ 'codeink = codeink_cli:main']}
)
