=======
CodeInk
=======
.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
    :alt: LICENSE
    :target: LICENSE

CodeInk is a Python source code analyzer focused on complexity and interrelation of modules.

CodeInk draws the ihnerent relations of your modules along with their complexity and maintanability indexes in a beautiful graph powered by D3.js and SVG elements.

![radon drawing made by CodeInk](radon_art.png)
- drawing of radon v1.2
- hover over a rounded rectangle to check which module is it

o.O?
====

the animations that CodeInk creates are base on:
* symbols: rounded squares are modules --> Python is a circle (hint: installed modules)
* lines: each line represents an import
* color: module maintainability index   green = :) --> red = :(
* size: ciclomatic complexity           small = :) --> big = :(

hint: if A imports B, and B imports C, then A imports B and C, right?
        A --> B, B --> C, A --> B & C

install::

    pip3 install git+https://github.com/carocad/CodeInk.git

usage
=====

draw a package structure::

    codeink draw /path/to/project

trace a module's imports::

    codeink trace /path/to/module.py

check who imports a module::

    codeink blame /path/to/module.py

get an overview of a module::

    codeink portrait /path/to/module.py

requirements
============
* python v3.3
* `docopt v0.6.2 <https://pypi.python.org/pypi/docopt>`_
* `networkx v1.9.1 <https://pypi.python.org/pypi/networkx/1.9.1>`_
* `radon v1.2 <https://pypi.python.org/pypi/radon/1.2.1>`_
* `astunparse v1.2 <https://pypi.python.org/pypi/astunparse/1.2.2>`_
* `D3.js <http://d3js.org>`_ (used automatically in the html head)

notes
=====
In order to use CodeInk you must make sure that your python version uses the same syntax as the code that you are analyzing i.e. analyzing a code written with Python v2.7 syntax while using Python v3.x will result in an error.

