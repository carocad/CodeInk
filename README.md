# codeInk
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

codeInk is a Python source code analyzer focused on complexity and interrelation of modules.

codeInk draws the ihnerent relations of your modules along with their complexity and maintanability indexes in a beautiful graph powered by D3.js and SVG elements.

![radon drawing made by codeInk](radon_art.png)
- drawing of radon v1.2
- hover over a rounded rectangle to check which module is it

## o.O?
the animations that codeInk creates are base on:
* symbols: rounded squares are modules --> Python is a circle (hint: installed modules)
* lines: each line represents an import
* color: module maintainability index   green = :) --> red = :(
* size: ciclomatic complexity           small = :) --> big = :(

hint: if A imports B, and B imports C, then A imports B and C, right? 
        A --> B, B --> C, A --> B & C

## install
```
pip3 install git+https://github.com/carocad/codeInk.git
```
## usage
### draw a package structure
```
$ codeink draw /path/to/project
```
### trace a module's imports
```
codeink trace /path/to/module.py
```
### check who imports a module
```
codeink blame /path/to/module.py
```

## requirements
* python v3.3 (previous versions not tested)
* docopt v0.6.2 ((previous versions not tested))
* networkx v1.9.1 (previous versions not tested)
* radon v1.2 (previous versions not tested)
* D3.js (used automatically in the html head)

### notes
radon uses the ast_tree to analyze python code, so if the code to be drawn is not compatible with your python version. codeInk will be a bunch of utilities without any meaning (ERROR).

