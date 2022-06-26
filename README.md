# MrMat :: Hello Python

Experiments in Python

## How this repository is organised

Almost all code is within `mrmat_hello_python`, along with the testsuite within `tests`. There are more tests than 
static code.

There is a namespaced package called `mrmat_hello_python_namespaced`. Namespace packages differ from regular packages
in that they do not have a `__init__.py` (although since it is no longer required for a Python package to have a
`__init__.py` it is probably difficult to distinguish between these). Namespace packages can be programmatically 
recognised because they have a different object for their loader than a regular package or module (NamespaceLoader vs
SourceFileLoader).

See [PEP420](https://peps.python.org/pep-0420/).
