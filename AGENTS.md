# Agent configuration for this project

## Preferences

* The project uses uv. Do not attempt to invoke pip directly.
* Use 'import package' or import 'package.sub-package' for dependencies, then fully qualify their use
* Use 'from package import symbol' for local imports

## Versioning

* The project uses MAJOR.MINOR.PATCH versioning
* The local version MUST always be 0.0.0.dev0. It is only when building the project in CI that the version is auto-generated.
* The project uses a dynamic version, as you can see in pyproject.toml. See the `src/ci` module how the version is obtained from the 'MRMAT_VERSION' environment variable during build-time. Note that the ci module is explicitly excluded from the package, it is exclusively used during build-time.
* During runtime, the project knows its version from the `__version__` attribute of the main package `__init__.py`

