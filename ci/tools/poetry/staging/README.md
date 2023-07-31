# Staging

This is the staging environment used by PEP-517 compliant builds of the project.
Here, the project is restructured into a single `ocebuild` package scope where
all module imports are rewritten to reflect the new root package scope.

This leverages the `poetry-core` backend in the project's `pyproject.toml` and
requires no additional configuration, ensuring that other PEP-517 frontends like
PIP can also build the project from source.
