# nikola
nikola is a crazy man that with will draw your python packages in his head.

He will use as many tools as possible to make his drawing comes true.

## o.O?
the animation that nikola creates is base on your several things:
* color: module maintainability index; green= :) --> reed= :(
* size: ciclomatic complexity; small= :) --> big= :(

each module is linked with every other module that it imports either directly or indirectly.

## mind-space
![alt tag](https://raw.github.com/carocad/nikola/master/radon_art.png)

## install
Coming soon

## requirements
* python v3 (previous versions not tested)
* networkx v1.9.1 (previous versions not tested)
* radon v1.2 (previous versions not tested)
* D3.js (used automatically in the html head)

## usage
```
$ cd my_project
$ nikola draw
```
more info comming soon

### lincense Apache 2.0

### notes
radon uses the ast_tree to analyze python code, so if the code to be drawn is not compatible with your python version. nikola will be just a crazy person without any meaning (ERROR).

