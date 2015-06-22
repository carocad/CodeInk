
from setuptools import setup, find_packages
import codeink

setup(
    name = 'codeink',
    version = codeink.__version__,
    description = 'codeink draws your Python source code into beautiful graph structures',
    long_description = open('README.rst').read(),
    author = codeink.__author__,
    author_email = codeink.__author_email__,
    license = codeink.__license__,
    keywords = ['graph', 'drawings', 'module', 'complexity',
                'maintainability', 'imports', 'structure'],
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
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Topic :: Software Development',
                    'Topic :: Software Development :: Quality Assurance',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.2',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4'],
    entry_points = {'console_scripts': [ 'codeink = codeink_cli:main']}
)
