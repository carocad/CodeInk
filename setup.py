
from setuptools import setup, find_packages
import src

setup(
    name = 'nicolas',
    version = src.__version__,
    description = 'nicolas draws your Python source code into beautiful graph structures',
    long_description = open('README.md').read(),
    author = src.__author__,
    author_email = src.__author_email__,
    license = src.__license__,
    keywords = ['graph', 'module', 'complexity', 'maintainability', 'import'],
    url = src.__URL__,
    packages = find_packages(),
	py_modules = ['nicolas_cli'],
	package_data = { 'src.canvas': ['hand.js',
							 		'canvas.html',
							 		'cubism.css'] },
    install_requires = ['docopt>=0.6.2',
						'networkx>=1.9.1',
						'radon>=1.2' ],
    classifiers = ['Development Status :: 3 - Alpha',
				 	'Topic :: Utilities',
				 	'Programming Language :: Python :: 3'],
    entry_points = {'console_scripts': [ 'nicolas = nicolas_cli:main']}
)
