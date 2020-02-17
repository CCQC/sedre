# sedre
A lightweight parser for computational quantum chemistry

## About
The name says it all, uses `sed` to slice up output into sections and Python's `re` module to grab information.
The parser is fully recursive, so it can handle sections, subsections, subsubsections, etc. Uses a giant "data" 
dictionary to store information, so use `.keys()` to navigate around. Final values will be in an entry marked `vals`.

```
import sedre
myp = sedre.Parser(program="psi4")
myp.data['energy'].keys()
```

## Install
### Dependencies
- Python standard library
- POSIX compliant `sed` program

### Add to pythonpath
add to e.g. your .bashrc, `export PYTHONPATH=PATH_TO_SEDRE:$PYTHONPATH`

### Run tests
in sedre/tests: `$ pytest`

Should see 1 fail 7 pass as of Feb 17 2020
