# General guideline for this cog

## Functions and methods
There should be no abstract methods, if it does not need instance variables it should not be in a class.
Classes should only exist if there needs to be instance variables.

## Imports
Always begin with `from __future__ import annotation`. Never have a module without this (except for an `__init__` file but :p).
For every other type of module always do `import module` and under `from module import CONSTANT sub_module, method, Class`:
    Base modules
    External modules
    Relative module