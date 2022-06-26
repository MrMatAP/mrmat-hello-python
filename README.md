# MrMat :: Hello Python

Experiments in Python

## How this repository is organised

Almost all code is within `mrmat_hello_python`, along with the testsuite within `tests`. There are more tests than 
static code.

There is a namespaced package called `mrmat_hello_python_namespaced`. Namespace packages differ from regular packages
in that they do not have a `__init__.py` (although since it is no longer required for a Python package to have a
`__init__.py` it is probably difficult to distinguish between these). Namespace packages can be programmatically 
recognised because they have a different object for their loader than a regular package or module (NamespaceLoader vs
SourceFileLoader). See [PEP420](https://peps.python.org/pep-0420/).

There is an executable directory called `mrmat-hello-python-executable`, which can be executed via `python 
mrmat-hello-python-executable`. Python looks for a `__main__.py` and will just execute it. Python will add the 
directory containing `__main__.py` to sys.path, which can be a useful distribution method. You can zip up the
contents of the directory (but not the directory itself). Python supports executing code directly from a zip file.

If you put `__main__.py` within a package then that package becomes executable via `python -m <package>`.
