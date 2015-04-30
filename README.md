# nicolas
nicolas is a crazy man that with will draw your python modules' relations, complexity and maintainability index in your webbrowser; and he will use as many tools as possible to make his drawings comes true.

![alt tag](radon_art.png)
- drawing of radon v1.2
- hover over a rounded rectangle to check which module is it

## o.O?
the animations that nicolas creates are base on:
* symbols: rounded squares are modules --> Python is a circle (hint: installed modules)
* lines: each line represents an import
* color: module maintainability index; green= :) --> red= :(
* size: ciclomatic complexity; small= :) --> big= :(

hint: if A imports B, and B imports C, then A imports B and C, right? 
        A --> B, B --> C, A --> B & C

## install
PIP Coming soon
### manually
```
$ git clone https://github.com/carocad/nicolas.git
$ cd nicolas
$ python setup.py install
```
## usage
```
$ nicolas draw /path/to/project
```
more info comming soon

## requirements
* python v3.3 (previous versions not tested)
* docopt v0.6.2 ((previous versions not tested))
* networkx v1.9.1 (previous versions not tested)
* radon v1.2 (previous versions not tested)
* D3.js (used automatically in the html head)

### lincense Apache 2.0

### notes
radon uses the ast_tree to analyze python code, so if the code to be drawn is not compatible with your python version. nikola will be just a crazy person without any meaning (ERROR).

