
from setuptools import setup, find_packages
import codeink

setup(
    name = 'codeInk',
    version = codeink.__version__,
    description = 'codeInk draws your Python source code into beautiful graph structures',
    long_description = open('README.rst').read(),
    author = codeink.__author__,
    author_email = codeink.__author_email__,
    license = codeink.__license__,
    keywords = ['graph', 'module', 'complexity', 'maintainability', 'import'],
    url = codeink.__URL__,
    packages = find_packages(),
	py_modules = ['codeink_cli'],
	package_data = { 'codeink.canvas': ['hand.js',
							 			'canvas.html',
							 			'cubism.css'] },
    install_requires = ['docopt>=0.6.2',
						'networkx>=1.9.1',
						'radon>=1.2',
					   	'astunparse>=1.2'],
    classifiers = [ 'Development Status :: 3 - Alpha',
				   	'Intended Audience :: Developers',
				 	'Topic :: Utilities',
				 	'Programming Language :: Python :: 3'],
    entry_points = {'console_scripts': [ 'codeink = codeink_cli:main']}
)
