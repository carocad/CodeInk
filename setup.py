
from setuptools import setup, find_packages
from src import __version__

setup(
    name = 'nikola',
    version = __version__,
    description = 'nikola draws your Python modules into a graph.',
    long_description = open('README.md').read(),
    author='Camilo Roca',
    author_email = 'carocad@unal.edu.co',
    license = 'Apache 2.0',
    keywords = ['graph', 'module', 'complexity', 'maintainability', 'import'],
    url = 'http://github.com/carocad/nikola',
    packages = find_packages(),
	data_files=[ ('src/canvas', ['src/canvas/canvas.html',
							 'src/canvas/hand.js',
							 'src/canvas/data.json',
							 'src/canvas/cubism.css']) ],
    install_requires = ['docopt>=0.6.2',
						'networkx>=1.9.1',
						'radon>=1.2' ],
    classifiers = ['Development Status :: 3 - Alpha',
				 'Topic :: Utilities',
				 'Programming Language :: Python :: 3'],
    entry_points = {'console_scripts': [
						'nikola = src:main']}
)
