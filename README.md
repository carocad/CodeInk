# nikola
nikola is a crazy man that with will draw your python packages in your webbrowser; and he will use as many tools as possible to make his drawings comes true.

## o.O?
the animation that nikola creates is base on:
* symbols: rounded squares are modules --> Python is a circle (hint: installed modules)
* lines: each line represents an import
* color: module maintainability index; green= :) --> red= :(
* size: ciclomatic complexity; small= :) --> big= :(

hint: if A imports B, and B imports C, then A imports B and C, right? 
        A --> B, B --> C, A --> B & C

## mind-space
![alt tag](https://raw.github.com/carocad/nikola/master/radon_art.png)
- drawing of radon v1.2
- hover over a rounded rectangle to check which module is it

## install
PIP Coming soon
### manually
```
$ git clone https://github.com/carocad/nikola.git
$ cd nikola
$ python setup.py install
```
## usage
```
$ cd my_project
$ sudo nikola draw
```
more info comming soon
NOTE: nikola needs to write a json file that will be later load using javascript. Currently I haven't found any other way to do this but to give special permissions to nikola once it is installed.

## requirements
* python v3 (previous versions not tested)
* docopt v0.6.2 ((previous versions not tested))
* networkx v1.9.1 (previous versions not tested)
* radon v1.2 (previous versions not tested)
* D3.js (used automatically in the html head)

### lincense Apache 2.0

### notes
radon uses the ast_tree to analyze python code, so if the code to be drawn is not compatible with your python version. nikola will be just a crazy person without any meaning (ERROR).

