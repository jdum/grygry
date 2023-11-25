# grygry

`grygry` is a set of command line utilities to grep different types of source code.

## Description

This script is for my own use, but if you are interested:

- The provided list of scripts find lines of source code in the current directory that match the argument string.
- Options are hardcoded in a parameters file (see `grygry/lib/parameters.json`).
- A list of script dynamically generated from the parameters file are available: gryall, grycfg, grycss, gryhtml, gryhtmlall, gryjs, gryjson, grymd, grynopy, grypy, grypy0, grypy2, gryrb, grysh, grytoml, grytxt, gryyml.
- Just look in the parameters file to understand the various options (and adapt to your needs.)

This project is licensed under the MIT License.

Project:
    https://github.com/jdum/grygry

Author:
    jerome.dumonteil@gmail.com


## Example

```shell
% grypy self.found
/Users/jd/dev/gits/grygry/grygry/lib/grylib.py
   20:         self.path = Path()
   21:         self.found = {}
   22:

   74:         self.find_word(path)
   75:         if not self.found:
   76:             return

...
```


## Installation

Installation from `Pypi` (recommended):


```python
pip install grypy
```
